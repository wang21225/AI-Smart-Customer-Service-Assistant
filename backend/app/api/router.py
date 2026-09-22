from fastapi import APIRouter

from app.api.routes import chat, config, conversations, dashboard, feedback, knowledge, tickets

api_router = APIRouter()
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(conversations.router, tags=["conversations"])
api_router.include_router(knowledge.router, tags=["knowledge"])
api_router.include_router(tickets.router, tags=["tickets"])
api_router.include_router(feedback.router, tags=["feedback"])
api_router.include_router(dashboard.router, tags=["dashboard"])
api_router.include_router(config.router, tags=["config"])
