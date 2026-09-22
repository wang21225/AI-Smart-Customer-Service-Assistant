from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ApiResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Any = None


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SourceInfo(BaseModel):
    document_id: int | None = None
    document_name: str
    page_no: int = 1
    score: float = 0
    snippet: str


class TimeMixinOut(ORMModel):
    id: int
    created_at: datetime
    updated_at: datetime
