from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.responses import success
from app.db.session import get_db
from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    return success(ChatService(db).chat(request).model_dump())


@router.post("/chat/stream")
def chat_stream(request: ChatRequest, db: Session = Depends(get_db)):
    return StreamingResponse(ChatService(db).stream(request), media_type="text/event-stream")
