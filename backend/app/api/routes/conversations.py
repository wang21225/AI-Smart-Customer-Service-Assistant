from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.responses import success
from app.db.session import get_db
from app.repositories.conversation_repo import ConversationRepository
from app.schemas.chat import ConversationCreate, ConversationOut, MessageOut

router = APIRouter(prefix="/conversations")


@router.get("")
def list_conversations(db: Session = Depends(get_db)):
    data = [ConversationOut.model_validate(item).model_dump() for item in ConversationRepository(db).list()]
    return success(data)


@router.post("")
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db)):
    item = ConversationRepository(db).create(payload.title, payload.customer_id)
    return success(ConversationOut.model_validate(item).model_dump())


@router.get("/{conversation_id}")
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    item = ConversationRepository(db).get(conversation_id)
    if not item:
        raise HTTPException(status_code=404, detail="会话不存在")
    return success(ConversationOut.model_validate(item).model_dump())


@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    ConversationRepository(db).delete(conversation_id)
    return success(True)


@router.get("/{conversation_id}/messages")
def list_messages(conversation_id: int, db: Session = Depends(get_db)):
    data = [MessageOut.model_validate(item).model_dump() for item in ConversationRepository(db).messages(conversation_id)]
    return success(data)
