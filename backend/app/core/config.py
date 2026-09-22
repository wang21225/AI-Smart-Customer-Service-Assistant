from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    dashscope_api_key: str = Field(default="", alias="DASHSCOPE_API_KEY")
    chat_model: str = Field(default="qwen-plus", alias="CHAT_MODEL")
    intent_model: str = Field(default="qwen-turbo", alias="INTENT_MODEL")
    embedding_model: str = Field(default="text-embedding-v3", alias="EMBEDDING_MODEL")
    mysql_host: str = Field(default="localhost", alias="MYSQL_HOST")
    mysql_port: int = Field(default=3306, alias="MYSQL_PORT")
    mysql_database: str = Field(default="ai_customer_service", alias="MYSQL_DATABASE")
    mysql_username: str = Field(default="root", alias="MYSQL_USERNAME")
    mysql_password: str = Field(default="123456", alias="MYSQL_PASSWORD")
    chroma_persist_dir: str = Field(default="./data/chroma", alias="CHROMA_PERSIST_DIR")
    upload_dir: str = Field(default="./data/uploads", alias="UPLOAD_DIR")
    rag_top_k: int = Field(default=3, alias="RAG_TOP_K")
    rag_score_threshold: float = Field(default=0.35, alias="RAG_SCORE_THRESHOLD")
    intent_confidence_threshold: float = Field(default=0.55, alias="INTENT_CONFIDENCE_THRESHOLD")
    backend_cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        alias="BACKEND_CORS_ORIGINS",
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_username}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
        )

    @property
    def cors_origins(self) -> list[str]:
        return [item.strip() for item in self.backend_cors_origins.split(",") if item.strip()]

    def ensure_dirs(self) -> None:
        Path(self.chroma_persist_dir).mkdir(parents=True, exist_ok=True)
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    value = Settings()
    value.ensure_dirs()
    return value


settings = get_settings()
