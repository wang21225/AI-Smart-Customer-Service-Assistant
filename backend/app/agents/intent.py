import json
import re

from app.agents.llm import get_chat_model
from app.core.config import settings


ORDER_PATTERN = re.compile(r"\b\d{10,20}\b")


def detect_intent(query: str) -> dict:
    order_no_match = ORDER_PATTERN.search(query)
    order_no = order_no_match.group(0) if order_no_match else ""
    lowered = query.lower()

    if any(word in query for word in ["人工", "客服", "真人"]):
        return {"intent": "human_service", "confidence": 0.95, "slots": {}, "reason": "用户明确要求人工客服"}
    if any(word in query for word in ["投诉", "不满", "差评"]):
        return {"intent": "complaint", "confidence": 0.93, "slots": {}, "reason": "用户表达投诉诉求"}
    if any(word in query for word in ["物流", "到哪里", "快递", "运单"]):
        return {"intent": "logistics_query", "confidence": 0.92, "slots": {"order_no": order_no}, "reason": "用户查询物流"}
    if any(word in query for word in ["订单", "购买", "支付"]):
        return {"intent": "order_query", "confidence": 0.88, "slots": {"order_no": order_no}, "reason": "用户查询订单"}

    policy_words = ["政策", "规则", "几天", "多久", "怎么", "如何", "可以", "能不能", "支持吗", "条件"]
    after_sales_words = ["退款", "退货", "售后", "换货", "保修"]
    if any(word in query for word in after_sales_words):
        if order_no and any(word in query for word in ["申请", "办理", "我要退款", "提交"]):
            return {"intent": "refund_request", "confidence": 0.9, "slots": {"order_no": order_no}, "reason": "用户提交退款或售后申请"}
        if any(word in query for word in policy_words) or not order_no:
            return {"intent": "faq_question", "confidence": 0.86, "slots": {}, "reason": "用户咨询售后政策，需要检索知识库"}
        return {"intent": "refund_request", "confidence": 0.82, "slots": {"order_no": order_no}, "reason": "用户表达退款售后诉求"}

    if any(word in query for word in policy_words):
        return {"intent": "faq_question", "confidence": 0.78, "slots": {}, "reason": "用户询问知识库问题"}
    if any(word in lowered for word in ["hi", "hello"]) or any(word in query for word in ["你好", "谢谢"]):
        return {"intent": "general_chat", "confidence": 0.82, "slots": {}, "reason": "普通闲聊"}

    model = get_chat_model(settings.intent_model, temperature=0)
    if model:
        prompt = (
            "请识别客服意图，返回 JSON，字段包含 intent, confidence, slots, reason。"
            "可选意图：general_chat, faq_question, order_query, logistics_query, refund_request, complaint, human_service, unknown。\n"
            f"用户问题：{query}"
        )
        try:
            result = model.invoke(prompt).content
            return json.loads(result)
        except Exception:
            pass
    return {"intent": "unknown", "confidence": 0.3, "slots": {}, "reason": "无法稳定判断意图"}
