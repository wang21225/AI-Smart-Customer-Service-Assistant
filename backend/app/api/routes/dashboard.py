from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.responses import success
from app.db.session import get_db
from app.models import ChatMessage, Conversation, CustomerFeedback, CustomerTicket, ModelCallLog

router = APIRouter(prefix="/dashboard")

LOCAL_TZ = ZoneInfo("Asia/Shanghai")
UTC_TZ = ZoneInfo("UTC")

INTENT_LABELS = {
    "general_chat": "普通闲聊",
    "faq_question": "知识库问答",
    "order_query": "订单查询",
    "logistics_query": "物流查询",
    "refund_request": "退款售后",
    "complaint": "投诉",
    "human_service": "人工转接",
    "unknown": "未识别",
}


def _local_day_to_utc_range(day: datetime) -> tuple[datetime, datetime]:
    start = day.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return (
        start.astimezone(UTC_TZ).replace(tzinfo=None),
        end.astimezone(UTC_TZ).replace(tzinfo=None),
    )


def _has_sources(sources: list | None) -> bool:
    return bool(sources and len(sources) > 0)


@router.get("/statistics")
def statistics(db: Session = Depends(get_db)):
    now = datetime.now(LOCAL_TZ)
    today_start, tomorrow_start = _local_day_to_utc_range(now)

    conversations = db.query(Conversation).count()
    today_conversations = (
        db.query(Conversation)
        .filter(Conversation.created_at >= today_start, Conversation.created_at < tomorrow_start)
        .count()
    )
    today_users = (
        db.query(func.count(func.distinct(Conversation.customer_id)))
        .filter(
            Conversation.created_at >= today_start,
            Conversation.created_at < tomorrow_start,
            Conversation.customer_id.isnot(None),
        )
        .scalar()
        or 0
    )
    tickets = db.query(CustomerTicket).count()
    human_transfer_conversations = (
        db.query(func.count(func.distinct(CustomerTicket.conversation_id)))
        .filter(CustomerTicket.conversation_id.isnot(None))
        .scalar()
        or 0
    )
    likes = db.query(CustomerFeedback).filter(CustomerFeedback.rating == "like").count()
    dislikes = db.query(CustomerFeedback).filter(CustomerFeedback.rating == "dislike").count()
    total_messages = db.query(ChatMessage).count()
    assistant_messages = db.query(ChatMessage.sources).filter(ChatMessage.role == "assistant").all()
    knowledge_hits = sum(1 for (sources,) in assistant_messages if _has_sources(sources))
    knowledge_hit_rate = 0 if not assistant_messages else round(knowledge_hits / len(assistant_messages) * 100, 2)
    model_calls = db.query(ModelCallLog).count()
    auto_rate = (
        0
        if conversations == 0
        else round(max(0, min(1, (conversations - human_transfer_conversations) / conversations)) * 100, 2)
    )

    return success(
        {
            "todayConversations": today_conversations,
            "todayUsers": today_users,
            "autoResolveRate": auto_rate,
            "humanTransfers": tickets,
            "avgResponseTime": None,
            "satisfaction": likes - dislikes,
            "knowledgeHitRate": knowledge_hit_rate,
            "likes": likes,
            "dislikes": dislikes,
            "totalMessages": total_messages,
            "modelCalls": model_calls,
        }
    )


@router.get("/trends")
def trends(db: Session = Depends(get_db)):
    today = datetime.now(LOCAL_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
    dates: list[str] = []
    sessions: list[int] = []

    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        start, end = _local_day_to_utc_range(day)
        dates.append(day.strftime("%m-%d"))
        sessions.append(
            db.query(Conversation)
            .filter(Conversation.created_at >= start, Conversation.created_at < end)
            .count()
        )

    raw_intents = (
        db.query(Conversation.last_intent, func.count(Conversation.id))
        .filter(Conversation.last_intent.isnot(None), Conversation.last_intent != "")
        .group_by(Conversation.last_intent)
        .order_by(func.count(Conversation.id).desc())
        .all()
    )
    intents = [
        {"name": INTENT_LABELS.get(intent, intent), "value": count}
        for intent, count in raw_intents
        if count
    ]

    return success({"dates": dates, "sessions": sessions, "intents": intents})
