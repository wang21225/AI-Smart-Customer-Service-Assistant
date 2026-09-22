from collections.abc import Generator
import json
import time

from sqlalchemy.orm import Session

from app.agents.intent import detect_intent
from app.agents.llm import get_chat_model
from app.core.config import settings
from app.graphs.customer_service_graph import run_customer_service_graph
from app.models import KnowledgeBase, ModelCallLog
from app.rag.retriever import retrieve
from app.repositories.conversation_repo import ConversationRepository
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ConversationRepository(db)

    def _get_or_create_conversation(self, request: ChatRequest):
        conv = self.repo.get(request.session_id) if request.session_id else None
        if conv is None:
            title = request.message[:30] or "新的客服会话"
            conv = self.repo.create(title=title, customer_id=request.customer_id)
        return conv

    @staticmethod
    def _sse(event: str, data: dict) -> str:
        return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

    @staticmethod
    def _should_use_rag(intent: str, slots: dict) -> bool:
        return intent == "faq_question" or (intent == "refund_request" and not slots.get("order_no"))

    @staticmethod
    def _rag_prompt(query: str, context: str) -> str:
        return (
            "你是企业售后客服。请只根据下面的知识库内容回答用户问题。"
            "如果资料不足以确认答案，要明确说明无法确认，不要编造政策、金额、时效或条件。"
            "回答要简洁、自然，并优先直接给结论。\n\n"
            f"知识库内容：\n{context}\n\n"
            f"用户问题：{query}"
        )

    def _log_model_call(self, scene: str, model_name: str, started_at: float, extra: dict | None = None) -> None:
        self.db.add(
            ModelCallLog(
                model_name=model_name,
                scene=scene,
                latency_ms=int((time.perf_counter() - started_at) * 1000),
                extra=extra or {},
            )
        )
        self.db.commit()

    def chat(self, request: ChatRequest) -> ChatResponse:
        conv = self._get_or_create_conversation(request)
        self.repo.add_message(conv.id, "user", request.message)
        state = run_customer_service_graph(self.db, conv.id, request.message)
        self.repo.add_message(
            conv.id,
            "assistant",
            state["final_answer"],
            intent=state["intent"],
            sources=[source.model_dump() for source in state.get("sources", [])],
            tool_results=state.get("tool_results", {}),
        )
        return ChatResponse(
            session_id=conv.id,
            answer=state["final_answer"],
            intent=state["intent"],
            confidence=state["confidence"],
            need_human=state["need_human"],
            sources=state.get("sources", []),
            tool_results=state.get("tool_results", {}),
        )

    def stream(self, request: ChatRequest) -> Generator[str, None, None]:
        yield self._sse("status", {"status": "正在理解用户问题..."})
        intent_result = detect_intent(request.message)
        intent = intent_result.get("intent", "unknown")
        confidence = float(intent_result.get("confidence", 0))
        slots = intent_result.get("slots", {}) or {}

        if self._should_use_rag(intent, slots):
            yield from self._stream_rag_answer(request, intent, confidence)
            return

        if intent == "general_chat":
            yield from self._stream_general_chat(request, intent, confidence)
            return

        for status in ["正在识别业务意图...", "正在调用业务工具...", "正在生成客服回复..."]:
            yield self._sse("status", {"status": status})
        response = self.chat(request)
        for char in response.answer:
            yield self._sse("token", {"token": char})
        yield self._sse("done", json.loads(response.model_dump_json()))

    def _stream_general_chat(self, request: ChatRequest, intent: str, confidence: float) -> Generator[str, None, None]:
        conv = self._get_or_create_conversation(request)
        self.repo.add_message(conv.id, "user", request.message)

        answer = ""
        model = get_chat_model(settings.chat_model)
        if model:
            yield self._sse("status", {"status": "正在调用阿里云百炼大模型..."})
            prompt = (
                "你是企业 AI 智能客服，请用自然、简洁的中文回答。"
                "你可以说明自己能帮助用户查询订单、物流、退款售后政策，也可以引导用户提出具体问题。\n\n"
                f"用户问题：{request.message}"
            )
            started_at = time.perf_counter()
            try:
                for chunk in model.stream(prompt):
                    token = getattr(chunk, "content", "") or ""
                    if not isinstance(token, str):
                        token = str(token)
                    if not token:
                        continue
                    answer += token
                    yield self._sse("token", {"token": token})
                self._log_model_call("general_chat", settings.chat_model, started_at, {"status": "success"})
            except Exception as exc:
                self._log_model_call("general_chat", settings.chat_model, started_at, {"status": "error", "error": str(exc)})

        if not answer:
            answer = "你好，我是 AI 智能客服。你可以咨询订单、物流、退款政策，也可以让我转接人工客服。"
            for char in answer:
                yield self._sse("token", {"token": char})

        self.repo.add_message(conv.id, "assistant", answer, intent=intent, sources=[], tool_results={})
        response = ChatResponse(
            session_id=conv.id,
            answer=answer,
            intent=intent,
            confidence=confidence,
            need_human=False,
            sources=[],
            tool_results={},
        )
        yield self._sse("done", json.loads(response.model_dump_json()))

    def _stream_rag_answer(self, request: ChatRequest, intent: str, confidence: float) -> Generator[str, None, None]:
        conv = self._get_or_create_conversation(request)
        self.repo.add_message(conv.id, "user", request.message)

        yield self._sse("status", {"status": "正在检索企业知识库..."})
        kb = self.db.query(KnowledgeBase).filter(KnowledgeBase.is_default.is_(True)).first() or self.db.query(KnowledgeBase).first()
        sources = []
        answer = ""

        if not kb:
            answer = "当前还没有可用知识库，请先在后台创建知识库并上传企业资料。"
        else:
            sources = retrieve(self.db, kb.id, request.message, settings.rag_top_k)
            if not sources:
                answer = "我暂时无法在企业知识库中确认这个问题的答案，因此不能编造售后规则。"
            else:
                context = "\n\n".join(
                    [f"来源：{source.document_name} 第 {source.page_no} 页\n{source.snippet}" for source in sources]
                )
                model = get_chat_model(settings.chat_model)
                if model:
                    yield self._sse("status", {"status": "正在调用阿里云百炼大模型..."})
                    prompt = self._rag_prompt(request.message, context)
                    started_at = time.perf_counter()
                    try:
                        for chunk in model.stream(prompt):
                            token = getattr(chunk, "content", "") or ""
                            if not isinstance(token, str):
                                token = str(token)
                            if not token:
                                continue
                            answer += token
                            yield self._sse("token", {"token": token})
                        self._log_model_call("rag_answer", settings.chat_model, started_at, {"status": "success", "sources": len(sources)})
                    except Exception as exc:
                        self._log_model_call(
                            "rag_answer",
                            settings.chat_model,
                            started_at,
                            {"status": "error", "error": str(exc), "sources": len(sources)},
                        )
                        if not answer:
                            answer = ""
                if not answer:
                    answer = "根据已检索到的知识库资料，相关内容如下：\n\n" + "\n\n".join(
                        [f"- [{source.document_name} 第 {source.page_no} 页] {source.snippet}" for source in sources]
                    )

        if answer and not sources:
            for char in answer:
                yield self._sse("token", {"token": char})
        elif answer and sources and "根据已检索到的知识库资料" in answer:
            for char in answer:
                yield self._sse("token", {"token": char})

        self.repo.add_message(
            conv.id,
            "assistant",
            answer,
            intent=intent,
            sources=[source.model_dump() for source in sources],
            tool_results={},
        )
        response = ChatResponse(
            session_id=conv.id,
            answer=answer,
            intent=intent,
            confidence=confidence,
            need_human=False,
            sources=sources,
            tool_results={},
        )
        yield self._sse("done", json.loads(response.model_dump_json()))
