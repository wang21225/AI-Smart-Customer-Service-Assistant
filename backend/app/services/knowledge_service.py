from pathlib import Path
import tempfile
from uuid import uuid4

from fastapi import UploadFile
from langchain_core.documents import Document as LCDocument
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import DocumentChunk, KnowledgeBase, KnowledgeDocument
from app.rag.document_loader import load_document
from app.rag.retriever import retrieve
from app.rag.splitter import split_pages
from app.rag.vector_store import get_chroma


class KnowledgeService:
    def __init__(self, db: Session):
        self.db = db

    def list_bases(self) -> list[KnowledgeBase]:
        return self.db.query(KnowledgeBase).order_by(KnowledgeBase.created_at.desc()).all()

    def create_base(self, name: str, description: str | None, is_default: bool = False) -> KnowledgeBase:
        item = KnowledgeBase(name=name, description=description, is_default=is_default)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_base(self, kb_id: int, **values) -> KnowledgeBase | None:
        item = self.db.get(KnowledgeBase, kb_id)
        if not item:
            return None
        for key, value in values.items():
            if value is not None:
                setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_base(self, kb_id: int) -> None:
        item = self.db.get(KnowledgeBase, kb_id)
        if item:
            self.db.delete(item)
            self.db.commit()

    def documents(self, kb_id: int) -> list[KnowledgeDocument]:
        return self.db.query(KnowledgeDocument).filter(KnowledgeDocument.knowledge_base_id == kb_id).all()

    async def upload_document(self, kb_id: int, file: UploadFile) -> KnowledgeDocument:
        suffix = Path(file.filename or "").suffix.lower()
        target_dir = Path(settings.upload_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        filename = f"kb_{kb_id}_{uuid4().hex}{suffix}"
        target = target_dir / filename
        content = await file.read()
        try:
            target.write_bytes(content)
        except PermissionError:
            # 本地沙箱或受限部署可能禁止写配置目录，降级到系统临时目录以保证上传流程不中断。
            fallback_dir = Path(tempfile.gettempdir()) / "ai_customer_service_uploads"
            fallback_dir.mkdir(parents=True, exist_ok=True)
            target = fallback_dir / filename
            target.write_bytes(content)
        doc = KnowledgeDocument(
            knowledge_base_id=kb_id,
            filename=file.filename or target.name,
            file_path=str(target),
            file_type=suffix.lstrip("."),
            status="pending",
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        self.rebuild_document(doc.id)
        return doc

    def rebuild_document(self, document_id: int) -> KnowledgeDocument:
        doc = self.db.get(KnowledgeDocument, document_id)
        if not doc:
            raise ValueError("文档不存在")
        try:
            doc.status = "parsing"
            self.db.commit()
            pages = load_document(doc.file_path)
            doc.status = "splitting"
            self.db.commit()
            chunks = split_pages(pages)
            self.db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).delete()
            vector_docs = []
            ids = []
            for chunk in chunks:
                chroma_id = f"doc_{doc.id}_{uuid4().hex}"
                row = DocumentChunk(
                    knowledge_base_id=doc.knowledge_base_id,
                    document_id=doc.id,
                    chroma_id=chroma_id,
                    content=chunk["content"],
                    page_no=chunk["page_no"],
                    token_count=len(chunk["content"]),
                )
                self.db.add(row)
                ids.append(chroma_id)
                vector_docs.append(
                    LCDocument(
                        page_content=chunk.get("question", chunk["content"]),
                        metadata={
                            "chroma_id": chroma_id,
                            "document_id": doc.id,
                            "document_name": doc.filename,
                            "page_no": chunk["page_no"],
                            "answer": chunk.get("answer", ""),
                        },
                    )
                )
            doc.status = "embedding"
            doc.chunk_count = len(chunks)
            self.db.commit()
            store = get_chroma(f"kb_{doc.knowledge_base_id}")
            if store and vector_docs:
                store.add_documents(vector_docs, ids=ids)
            doc.status = "completed"
            doc.error_message = None
        except Exception as exc:
            doc.status = "failed"
            doc.error_message = str(exc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def test_retrieval(self, kb_id: int, query: str, top_k: int):
        return retrieve(self.db, kb_id, query, top_k)
