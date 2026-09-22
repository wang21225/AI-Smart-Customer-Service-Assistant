from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.responses import success
from app.db.session import get_db
from app.models import CustomerFeedback

router = APIRouter()


class FeedbackCreate(BaseModel):
    conversation_id: int
    message_id: int | None = None
    rating: str
    comment: str | None = None


@router.post("/feedback")
def create_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    item = CustomerFeedback(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return success({"id": item.id})
