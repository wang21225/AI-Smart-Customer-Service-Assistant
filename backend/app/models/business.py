from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Customer(TimestampMixin, Base):
    __tablename__ = "customer"

    name: Mapped[str] = mapped_column(String(80), index=True)
    phone: Mapped[str | None] = mapped_column(String(32), index=True)
    email: Mapped[str | None] = mapped_column(String(120))
    level: Mapped[str] = mapped_column(String(32), default="normal")

    conversations = relationship("Conversation", back_populates="customer")


class Product(TimestampMixin, Base):
    __tablename__ = "product"

    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    product_type: Mapped[str] = mapped_column(String(64), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)


class CustomerOrder(TimestampMixin, Base):
    __tablename__ = "customer_order"
    __table_args__ = (Index("idx_order_customer_status", "customer_id", "status"),)

    order_no: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime)

    customer = relationship("Customer")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    logistics = relationship("LogisticsRecord", back_populates="order", cascade="all, delete-orphan")


class OrderItem(TimestampMixin, Base):
    __tablename__ = "order_item"

    order_id: Mapped[int] = mapped_column(ForeignKey("customer_order.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), index=True)
    quantity: Mapped[int] = mapped_column(default=1)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)

    order = relationship("CustomerOrder", back_populates="items")
    product = relationship("Product")


class LogisticsRecord(TimestampMixin, Base):
    __tablename__ = "logistics_record"
    __table_args__ = (Index("idx_logistics_order_time", "order_id", "event_time"),)

    order_id: Mapped[int] = mapped_column(ForeignKey("customer_order.id"), index=True)
    company: Mapped[str] = mapped_column(String(80))
    tracking_no: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(64), index=True)
    location: Mapped[str] = mapped_column(String(160))
    detail: Mapped[str] = mapped_column(Text)
    event_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    order = relationship("CustomerOrder", back_populates="logistics")


class RefundRequest(TimestampMixin, Base):
    __tablename__ = "refund_request"

    request_no: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("customer_order.id"), index=True)
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
