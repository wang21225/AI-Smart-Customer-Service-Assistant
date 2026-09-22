from sqlalchemy import Boolean, ForeignKey, Float, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class KnowledgeBase(TimestampMixin, Base):
    __tablename__ = "knowledge_base"

    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    documents = relationship("KnowledgeDocument", back_populates="knowledge_base", cascade="all, delete-orphan")


class KnowledgeDocument(TimestampMixin, Base):
    __tablename__ = "knowledge_document"
    __table_args__ = (Index("idx_document_kb_status", "knowledge_base_id", "status"),)

    knowledge_base_id: Mapped[int] = mapped_column(ForeignKey("knowledge_base.id"), index=True)
    filename: Mapped[str] = mapped_column(String(255), index=True)
    file_path: Mapped[str] = mapped_column(String(500))
    file_type: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    knowledge_base = relationship("KnowledgeBase", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(TimestampMixin, Base):
    __tablename__ = "document_chunk"
    __table_args__ = (Index("idx_chunk_document_page", "document_id", "page_no"),)

    knowledge_base_id: Mapped[int] = mapped_column(ForeignKey("knowledge_base.id"), index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("knowledge_document.id"), index=True)
    chroma_id: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    page_no: Mapped[int] = mapped_column(Integer, default=1)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)

    document = relationship("KnowledgeDocument", back_populates="chunks")
