from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CustomerTicket(TimestampMixin, Base):
    __tablename__ = "customer_ticket"

    ticket_no: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    conversation_id: Mapped[int | None] = mapped_column(ForeignKey("conversation.id"), nullable=True, index=True)
    category: Mapped[str] = mapped_column(String(64), index=True)
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="open", index=True)
    priority: Mapped[str] = mapped_column(String(32), default="normal")
    ai_operations: Mapped[dict | None] = mapped_column(JSON, nullable=True)
