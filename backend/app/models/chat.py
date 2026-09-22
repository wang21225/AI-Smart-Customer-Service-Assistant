from sqlalchemy import Boolean, ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Conversation(TimestampMixin, Base):
    __tablename__ = "conversation"
    __table_args__ = (Index("idx_conversation_customer", "customer_id", "created_at"),)

    title: Mapped[str] = mapped_column(String(160), default="新的客服会话")
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customer.id"), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    last_intent: Mapped[str | None] = mapped_column(String(64), nullable=True)
    need_human: Mapped[bool] = mapped_column(Boolean, default=False)

    customer = relationship("Customer", back_populates="conversations")
    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan")


class ChatMessage(TimestampMixin, Base):
    __tablename__ = "chat_message"
    __table_args__ = (Index("idx_message_conversation_time", "conversation_id", "created_at"),)

    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversation.id"), index=True)
    role: Mapped[str] = mapped_column(String(32), index=True)
    content: Mapped[str] = mapped_column(Text)
    intent: Mapped[str | None] = mapped_column(String(64), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)
    tool_results: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    liked: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    conversation = relationship("Conversation", back_populates="messages")


class ConversationSummary(TimestampMixin, Base):
    __tablename__ = "conversation_summary"

    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversation.id"), unique=True, index=True)
    summary: Mapped[str] = mapped_column(Text)
    key_facts: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class CustomerProfile(TimestampMixin, Base):
    __tablename__ = "customer_profile"

    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"), unique=True, index=True)
    preferences: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    risk_tags: Mapped[list | None] = mapped_column(JSON, nullable=True)


class CustomerFeedback(TimestampMixin, Base):
    __tablename__ = "customer_feedback"

    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversation.id"), index=True)
    message_id: Mapped[int | None] = mapped_column(ForeignKey("chat_message.id"), nullable=True)
    rating: Mapped[str] = mapped_column(String(16), index=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
