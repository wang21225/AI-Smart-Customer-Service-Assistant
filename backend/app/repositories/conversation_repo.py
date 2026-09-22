from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import ChatMessage, Conversation, ConversationSummary, CustomerFeedback, CustomerTicket


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Conversation]:
        return self.db.query(Conversation).order_by(Conversation.updated_at.desc()).all()

    def get(self, conversation_id: int) -> Conversation | None:
        return self.db.get(Conversation, conversation_id)

    def create(self, title: str, customer_id: int | None = None) -> Conversation:
        item = Conversation(title=title, customer_id=customer_id)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, conversation_id: int) -> None:
        item = self.get(conversation_id)
        if item:
            self.db.query(CustomerFeedback).filter(CustomerFeedback.conversation_id == conversation_id).delete(synchronize_session=False)
            self.db.query(ConversationSummary).filter(ConversationSummary.conversation_id == conversation_id).delete(synchronize_session=False)
            self.db.query(CustomerTicket).filter(CustomerTicket.conversation_id == conversation_id).update(
                {CustomerTicket.conversation_id: None},
                synchronize_session=False,
            )
            self.db.delete(item)
            self.db.commit()

    def messages(self, conversation_id: int) -> list[ChatMessage]:
        return (
            self.db.query(ChatMessage)
            .filter(ChatMessage.conversation_id == conversation_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )

    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        intent: str | None = None,
        sources: list | None = None,
        tool_results: dict | None = None,
    ) -> ChatMessage:
        item = ChatMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
            intent=intent,
            sources=sources,
            tool_results=tool_results,
        )
        self.db.add(item)
        conv = self.get(conversation_id)
        if conv:
            conv.last_intent = intent or conv.last_intent
            conv.need_human = bool(tool_results and tool_results.get("need_human"))
        self.db.commit()
        self.db.refresh(item)
        return item
