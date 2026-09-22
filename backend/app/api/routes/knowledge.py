from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.responses import success
from app.db.session import get_db
from app.models import DocumentChunk, KnowledgeDocument
from app.schemas.knowledge import (
    KnowledgeBaseCreate,
    KnowledgeBaseOut,
    KnowledgeBaseUpdate,
    KnowledgeDocumentOut,
    RetrievalTestRequest,
    RetrievalTestResponse,
)
from app.services.knowledge_service import KnowledgeService

router = APIRouter()


@router.get("/knowledge-bases")
def list_knowledge_bases(db: Session = Depends(get_db)):
    items = KnowledgeService(db).list_bases()
    return success([KnowledgeBaseOut.model_validate(item).model_dump() for item in items])


@router.post("/knowledge-bases")
def create_knowledge_base(payload: KnowledgeBaseCreate, db: Session = Depends(get_db)):
    item = KnowledgeService(db).create_base(payload.name, payload.description, payload.is_default)
    return success(KnowledgeBaseOut.model_validate(item).model_dump())


@router.put("/knowledge-bases/{kb_id}")
def update_knowledge_base(kb_id: int, payload: KnowledgeBaseUpdate, db: Session = Depends(get_db)):
    item = KnowledgeService(db).update_base(kb_id, **payload.model_dump())
    if not item:
        raise HTTPException(status_code=404, detail="知识库不存在")
    return success(KnowledgeBaseOut.model_validate(item).model_dump())


@router.delete("/knowledge-bases/{kb_id}")
def delete_knowledge_base(kb_id: int, db: Session = Depends(get_db)):
    KnowledgeService(db).delete_base(kb_id)
    return success(True)


@router.post("/knowledge-bases/{kb_id}/documents")
async def upload_document(kb_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    item = await KnowledgeService(db).upload_document(kb_id, file)
    return success(KnowledgeDocumentOut.model_validate(item).model_dump())


@router.get("/knowledge-bases/{kb_id}/documents")
def list_documents(kb_id: int, db: Session = Depends(get_db)):
    items = KnowledgeService(db).documents(kb_id)
    return success([KnowledgeDocumentOut.model_validate(item).model_dump() for item in items])


@router.get("/documents/{document_id}/chunks")
def list_document_chunks(document_id: int, db: Session = Depends(get_db)):
    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.page_no.asc(), DocumentChunk.id.asc())
        .all()
    )
    return success(
        [
            {
                "id": item.id,
                "document_id": item.document_id,
                "page_no": item.page_no,
                "content": item.content,
                "token_count": item.token_count,
                "score": item.score,
                "created_at": item.created_at,
            }
            for item in chunks
        ]
    )


@router.delete("/documents/{document_id}/chunks")
def delete_document_chunks(document_id: int, db: Session = Depends(get_db)):
    deleted = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete(synchronize_session=False)
    document = db.get(KnowledgeDocument, document_id)
    if document:
        document.chunk_count = 0
        document.status = "completed"
    db.commit()
    return success({"deleted": deleted})


@router.delete("/chunks/{chunk_id}")
def delete_chunk(chunk_id: int, db: Session = Depends(get_db)):
    chunk = db.get(DocumentChunk, chunk_id)
    if not chunk:
        return success({"deleted": 0})
    document_id = chunk.document_id
    db.delete(chunk)
    db.flush()
    document = db.get(KnowledgeDocument, document_id)
    if document:
        document.chunk_count = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).count()
    db.commit()
    return success({"deleted": 1, "document_id": document_id, "chunk_count": document.chunk_count if document else 0})


@router.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    item = db.get(KnowledgeDocument, document_id)
    if item:
        db.delete(item)
        db.commit()
    return success(True)


@router.post("/documents/{document_id}/rebuild")
def rebuild_document(document_id: int, db: Session = Depends(get_db)):
    item = KnowledgeService(db).rebuild_document(document_id)
    return success(KnowledgeDocumentOut.model_validate(item).model_dump())


@router.post("/retrieval/test")
def retrieval_test(payload: RetrievalTestRequest, db: Session = Depends(get_db)):
    results = KnowledgeService(db).test_retrieval(payload.knowledge_base_id, payload.query, payload.top_k)
    return success(RetrievalTestResponse(query=payload.query, results=results).model_dump())
