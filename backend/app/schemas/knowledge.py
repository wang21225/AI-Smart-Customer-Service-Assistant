from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel, SourceInfo


class KnowledgeBaseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    is_default: bool = False


class KnowledgeBaseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_default: bool | None = None


class KnowledgeBaseOut(ORMModel):
    id: int
    name: str
    description: str | None
    is_default: bool
    created_at: datetime
    updated_at: datetime


class KnowledgeDocumentOut(ORMModel):
    id: int
    knowledge_base_id: int
    filename: str
    file_type: str
    status: str
    chunk_count: int
    error_message: str | None
    created_at: datetime


class RetrievalTestRequest(BaseModel):
    knowledge_base_id: int
    query: str = Field(min_length=1)
    top_k: int = 3


class RetrievalTestResponse(BaseModel):
    query: str
    results: list[SourceInfo]
