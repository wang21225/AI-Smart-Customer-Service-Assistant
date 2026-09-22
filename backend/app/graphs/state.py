from typing import Any, TypedDict

from langchain_core.messages import BaseMessage


class CustomerServiceState(TypedDict, total=False):
    messages: list[BaseMessage]
    session_id: int
    user_query: str
    rewritten_query: str
    intent: str
    slots: dict[str, Any]
    confidence: float
    retrieved_documents: list
    tool_results: dict[str, Any]
    final_answer: str
    need_human: bool
    sources: list
