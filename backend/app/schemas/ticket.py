from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class TicketCreate(BaseModel):
    category: str
    content: str
    conversation_id: int | None = None
    priority: str = "normal"


class TicketUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None


class TicketOut(ORMModel):
    id: int
    ticket_no: str
    conversation_id: int | None
    category: str
    content: str
    status: str
    priority: str
    created_at: datetime
