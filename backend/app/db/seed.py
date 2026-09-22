from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import (
    Customer,
    CustomerOrder,
    KnowledgeBase,
    LogisticsRecord,
    OrderItem,
    Product,
    PromptTemplate,
    SystemConfig,
)


def seed_demo_data(db: Session) -> None:
    if db.query(Customer).first():
        return

    customer = Customer(name="演示用户", phone="13800000000", email="demo@example.com", level="vip")
    product = Product(sku="SKU-HELP-001", name="智能客服旗舰版", product_type="software", price=Decimal("3999.00"))
    db.add_all([customer, product])
    db.flush()

    order = CustomerOrder(
        order_no="202607160001",
        customer_id=customer.id,
        status="shipping",
        total_amount=Decimal("3999.00"),
        paid_at=datetime.utcnow() - timedelta(days=2),
    )
    db.add(order)
    db.flush()
    db.add(OrderItem(order_id=order.id, product_id=product.id, quantity=1, unit_price=Decimal("3999.00")))
    db.add_all(
        [
            LogisticsRecord(
                order_id=order.id,
                company="顺丰速运",
                tracking_no="SF202607160001",
                status="运输中",
                location="上海转运中心",
                detail="快件已到达上海转运中心，准备发往目的城市。",
                event_time=datetime.utcnow() - timedelta(hours=6),
            ),
            LogisticsRecord(
                order_id=order.id,
                company="顺丰速运",
                tracking_no="SF202607160001",
                status="已揽收",
                location="杭州滨江营业点",
                detail="顺丰已揽收，正在发往上海转运中心。",
                event_time=datetime.utcnow() - timedelta(days=1),
            ),
        ]
    )
    db.add(KnowledgeBase(name="默认售后知识库", description="用于演示售后政策、退款规则和常见问题。", is_default=True))
    db.add_all(
        [
            SystemConfig(config_key="intent_threshold", config_value="0.55", description="意图识别最低置信度"),
            PromptTemplate(
                name="rag_answer",
                scene="rag",
                content="只能根据企业知识库回答；资料不足时明确告知无法确认；回答中标明引用来源。",
            ),
        ]
    )
    db.commit()
