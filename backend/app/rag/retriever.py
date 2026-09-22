from rank_bm25 import BM25Okapi
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import DocumentChunk, KnowledgeDocument
from app.rag.vector_store import get_chroma
from app.schemas.common import SourceInfo


def _search_text(content: str) -> str:
    if content.startswith("问题：") and "\n答案：" in content:
        return content.split("\n答案：", 1)[0].replace("问题：", "").strip()
    return content


def retrieve(db: Session, knowledge_base_id: int, query: str, top_k: int | None = None) -> list[SourceInfo]:
    top_k = min(top_k or settings.rag_top_k, 3)
    chunks = db.query(DocumentChunk).filter(DocumentChunk.knowledge_base_id == knowledge_base_id).all()
    by_id = {chunk.chroma_id: chunk for chunk in chunks}
    scored: dict[int, float] = {}

    vector_store = get_chroma(f"kb_{knowledge_base_id}")
    if vector_store:
        for doc, score in vector_store.similarity_search_with_relevance_scores(query, k=top_k * 2):
            chroma_id = doc.metadata.get("chroma_id")
            chunk = by_id.get(chroma_id)
            if chunk and score >= settings.rag_score_threshold:
                scored[chunk.id] = max(scored.get(chunk.id, 0), float(score))

    if chunks:
        tokenized = [list(_search_text(chunk.content)) for chunk in chunks]
        bm25 = BM25Okapi(tokenized)
        scores = bm25.get_scores(list(query))
        for chunk, score in sorted(zip(chunks, scores), key=lambda item: item[1], reverse=True)[: top_k * 2]:
            if score > 0:
                scored[chunk.id] = max(scored.get(chunk.id, 0), min(float(score) / 10, 0.95))

    if chunks and not scored:
        query_chars = {char for char in query if char.strip()}
        for chunk in chunks:
            overlap = len(query_chars & {char for char in _search_text(chunk.content) if char.strip()})
            if overlap:
                scored[chunk.id] = min(overlap / max(len(query_chars), 1), 0.85)

    results = []
    for chunk_id, score in sorted(scored.items(), key=lambda item: item[1], reverse=True)[:top_k]:
        chunk = db.get(DocumentChunk, chunk_id)
        if not chunk:
            continue
        doc = db.get(KnowledgeDocument, chunk.document_id)
        results.append(
            SourceInfo(
                document_id=doc.id if doc else None,
                document_name=doc.filename if doc else "未知文档",
                page_no=chunk.page_no,
                score=round(score, 4),
                snippet=chunk.content[:500],
            )
        )
    return results
