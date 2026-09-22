from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class SystemConfig(TimestampMixin, Base):
    __tablename__ = "system_config"

    config_key: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    config_value: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class PromptTemplate(TimestampMixin, Base):
    __tablename__ = "prompt_template"

    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    scene: Mapped[str] = mapped_column(String(80), index=True)
    content: Mapped[str] = mapped_column(Text)
    version: Mapped[int] = mapped_column(Integer, default=1)


class ModelCallLog(TimestampMixin, Base):
    __tablename__ = "model_call_log"

    model_name: Mapped[str] = mapped_column(String(120), index=True)
    scene: Mapped[str] = mapped_column(String(80), index=True)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    extra: Mapped[dict | None] = mapped_column(JSON, nullable=True)
