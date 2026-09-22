from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel, SourceInfo


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: int | None = None
    customer_id: int | None = None


class ChatResponse(BaseModel):
    session_id: int
    answer: str
    intent: str
    confidence: float
    need_human: bool = False
    sources: list[SourceInfo] = []
    tool_results: dict[str, Any] = {}


class ConversationCreate(BaseModel):
    title: str = "新的客服会话"
    customer_id: int | None = None


class ConversationOut(ORMModel):
    id: int
    title: str
    customer_id: int | None
    status: str
    last_intent: str | None
    need_human: bool
    created_at: datetime
    updated_at: datetime


class MessageOut(ORMModel):
    id: int
    conversation_id: int
    role: str
    content: str
    intent: str | None = None
    sources: list | None = None
    tool_results: dict | None = None
    liked: bool | None = None
    created_at: datetime
