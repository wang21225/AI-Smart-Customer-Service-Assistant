from langgraph.graph import END, StateGraph
from sqlalchemy.orm import Session

from app.agents.intent import detect_intent
from app.agents.llm import get_chat_model
from app.core.config import settings
from app.graphs.state import CustomerServiceState
from app.models import KnowledgeBase
from app.rag.retriever import retrieve
from app.tools.business_tools import (
    create_customer_ticket,
    create_refund_request,
    query_logistics,
    query_order,
    query_refund_policy,
    transfer_to_human,
)


def load_context(state: CustomerServiceState) -> CustomerServiceState:
    state["rewritten_query"] = state["user_query"].strip()
    return state


def identify_intent(state: CustomerServiceState) -> CustomerServiceState:
    result = detect_intent(state["rewritten_query"])
    state["intent"] = result["intent"]
    state["confidence"] = float(result.get("confidence", 0))
    state["slots"] = result.get("slots", {})
    return state


def route(state: CustomerServiceState) -> str:
    if state.get("confidence", 0) < settings.intent_confidence_threshold:
        return "fallback"
    intent = state.get("intent", "unknown")
    if intent == "refund_request" and not state.get("slots", {}).get("order_no"):
        return "rag_answer"
    if intent in {"order_query", "logistics_query", "refund_request", "complaint", "human_service"}:
        return "business_tool"
    if intent == "faq_question":
        return "rag_answer"
    if intent == "general_chat":
        return "general_chat"
    return "fallback"


def make_business_tool_node(db: Session):
    def business_tool(state: CustomerServiceState) -> CustomerServiceState:
        intent = state["intent"]
        slots = state.get("slots", {})
        query = state["rewritten_query"]
        order_no = slots.get("order_no") or ""
        if intent == "logistics_query":
            result = query_logistics(db, order_no)
            state["tool_results"] = {"logistics": result}
            if result.get("found"):
                tracks = "\n".join([f"- {t['time']} {t['location']}：{t['detail']}" for t in result["tracks"]])
                state["final_answer"] = f"已查询到订单 {order_no} 的物流信息：\n\n物流公司：{result['company']}\n运单号：{result['tracking_no']}\n当前状态：{result['current_status']}\n\n物流轨迹：\n{tracks}"
            else:
                state["final_answer"] = result["message"]
        elif intent == "order_query":
            result = query_order(db, order_no)
            state["tool_results"] = {"order": result}
            state["final_answer"] = f"订单 {order_no} 当前状态为 {result.get('status')}，订单金额 {result.get('total_amount')} 元。" if result.get("found") else result["message"]
        elif intent == "refund_request":
            if order_no:
                result = create_refund_request(db, order_no, query)
                state["tool_results"] = {"refund": result}
                state["final_answer"] = f"已为你创建退款申请，申请编号：{result['request_no']}，当前状态：{result['status']}。" if result.get("created") else result["message"]
            else:
                result = query_refund_policy(db, "default")
                state["tool_results"] = {"refund_policy": result}
                state["final_answer"] = result["policy"] + "\n\n如需提交退款申请，请补充订单编号和退款原因。"
        elif intent == "complaint":
            result = create_customer_ticket(db, "complaint", query, state["session_id"])
            state["tool_results"] = result
            state["need_human"] = True
            state["final_answer"] = f"已为你创建投诉工单 {result['ticket_no']}，客服会尽快处理。"
        else:
            result = transfer_to_human(db, state["session_id"], query)
            state["tool_results"] = result
            state["need_human"] = True
            state["final_answer"] = f"已为你转接人工客服，工单编号 {result['ticket_no']}，请稍候。"
        return state

    return business_tool


def make_rag_node(db: Session):
    def rag_answer(state: CustomerServiceState) -> CustomerServiceState:
        kb = db.query(KnowledgeBase).filter(KnowledgeBase.is_default.is_(True)).first() or db.query(KnowledgeBase).first()
        if not kb:
            state["final_answer"] = "当前还没有可用知识库，请先在后台创建知识库并上传企业资料。"
            state["sources"] = []
            return state
        sources = retrieve(db, kb.id, state["rewritten_query"], settings.rag_top_k)
        state["sources"] = sources
        if not sources:
            state["final_answer"] = "我暂时无法在企业知识库中确认这个问题的答案，因此不能编造政策、价格、时间或售后规则。"
            return state
        context = "\n\n".join([f"来源：{s.document_name} 第{s.page_no}页\n{s.snippet}" for s in sources])
        model = get_chat_model(settings.chat_model)
        if model:
            prompt = f"只能根据以下企业知识库内容回答，并标明引用来源。资料不足时说无法确认。\n\n{context}\n\n用户问题：{state['rewritten_query']}"
            state["final_answer"] = model.invoke(prompt).content
        else:
            state["final_answer"] = "根据已检索到的知识库资料，相关内容如下：\n\n" + "\n\n".join(
                [f"- [{s.document_name} 第{s.page_no}页] {s.snippet}" for s in sources]
            )
        return state

    return rag_answer


def general_chat(state: CustomerServiceState) -> CustomerServiceState:
    state["final_answer"] = "你好，我是 AI 智能客服。你可以咨询订单、物流、退款政策，也可以让我转接人工客服。"
    return state


def fallback(state: CustomerServiceState) -> CustomerServiceState:
    state["need_human"] = True
    state["final_answer"] = "抱歉，我还不能准确判断你的问题。为了避免误导，建议补充订单号或更具体的问题，我也可以为你转接人工客服。"
    return state


def quality_check(state: CustomerServiceState) -> CustomerServiceState:
    state.setdefault("tool_results", {})
    state.setdefault("sources", [])
    state.setdefault("need_human", False)
    return state


def build_graph(db: Session):
    graph = StateGraph(CustomerServiceState)
    graph.add_node("load_context", load_context)
    graph.add_node("identify_intent", identify_intent)
    graph.add_node("business_tool", make_business_tool_node(db))
    graph.add_node("rag_answer", make_rag_node(db))
    graph.add_node("general_chat", general_chat)
    graph.add_node("fallback", fallback)
    graph.add_node("quality_check", quality_check)
    graph.set_entry_point("load_context")
    graph.add_edge("load_context", "identify_intent")
    graph.add_conditional_edges("identify_intent", route)
    for node in ["business_tool", "rag_answer", "general_chat", "fallback"]:
        graph.add_edge(node, "quality_check")
    graph.add_edge("quality_check", END)
    return graph.compile()


def run_customer_service_graph(db: Session, session_id: int, user_query: str) -> CustomerServiceState:
    app = build_graph(db)
    return app.invoke(
        {
            "messages": [],
            "session_id": session_id,
            "user_query": user_query,
            "tool_results": {},
            "sources": [],
            "need_human": False,
        }
    )
