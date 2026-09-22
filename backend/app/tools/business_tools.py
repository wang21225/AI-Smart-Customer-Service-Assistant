from datetime import datetime
from uuid import uuid4

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.models import CustomerOrder, CustomerTicket, LogisticsRecord, RefundRequest


def query_order(db: Session, order_no: str) -> dict:
    order = db.query(CustomerOrder).filter(CustomerOrder.order_no == order_no).first()
    if not order:
        return {"found": False, "message": "未找到该订单"}
    return {
        "found": True,
        "order_no": order.order_no,
        "status": order.status,
        "total_amount": float(order.total_amount),
        "paid_at": order.paid_at.isoformat() if order.paid_at else None,
    }


def query_logistics(db: Session, order_no: str) -> dict:
    order = db.query(CustomerOrder).filter(CustomerOrder.order_no == order_no).first()
    if not order:
        return {"found": False, "message": "未找到该订单，无法查询物流"}
    records = (
        db.query(LogisticsRecord)
        .filter(LogisticsRecord.order_id == order.id)
        .order_by(LogisticsRecord.event_time.desc())
        .all()
    )
    return {
        "found": True,
        "order_no": order.order_no,
        "company": records[0].company if records else "",
        "tracking_no": records[0].tracking_no if records else "",
        "current_status": records[0].status if records else order.status,
        "tracks": [
            {
                "time": item.event_time.isoformat(),
                "location": item.location,
                "status": item.status,
                "detail": item.detail,
            }
            for item in records
        ],
    }


def query_refund_policy(_: Session, product_type: str) -> dict:
    policies = {
        "software": "软件类商品签收后 7 天内，如未激活且不影响二次销售，可申请退款。",
        "default": "普通商品签收后 7 天内可申请无理由退货，特殊商品以页面说明为准。",
    }
    return {"product_type": product_type, "policy": policies.get(product_type, policies["default"])}


def create_refund_request(db: Session, order_no: str, reason: str) -> dict:
    order = db.query(CustomerOrder).filter(CustomerOrder.order_no == order_no).first()
    if not order:
        return {"created": False, "message": "未找到该订单，无法创建退款申请"}
    request = RefundRequest(request_no=f"RF{datetime.utcnow():%Y%m%d%H%M%S}{uuid4().hex[:6]}", order_id=order.id, reason=reason)
    db.add(request)
    db.commit()
    db.refresh(request)
    return {"created": True, "request_no": request.request_no, "status": request.status}


def create_customer_ticket(db: Session, category: str, content: str, conversation_id: int | None = None) -> dict:
    ticket = CustomerTicket(
        ticket_no=f"TK{datetime.utcnow():%Y%m%d%H%M%S}{uuid4().hex[:6]}",
        conversation_id=conversation_id,
        category=category,
        content=content,
        priority="high" if category in {"complaint", "human_service"} else "normal",
        ai_operations={"created_by": "ai_agent"},
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return {"ticket_no": ticket.ticket_no, "status": ticket.status, "need_human": True}


def transfer_to_human(db: Session, session_id: int, reason: str) -> dict:
    return create_customer_ticket(db, "human_service", reason, session_id)


@tool
def query_order_tool(order_no: str) -> str:
    """查询订单基础信息。实际 API 中使用注入数据库版本。"""
    return f"需要查询订单 {order_no}"
