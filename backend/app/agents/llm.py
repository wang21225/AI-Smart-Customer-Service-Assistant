from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_chat_model(model_name: str | None = None, temperature: float = 0.2) -> ChatOpenAI | None:
    if not settings.dashscope_api_key or settings.dashscope_api_key == "请用户自行填写":
        return None
    return ChatOpenAI(
        model=model_name or settings.chat_model,
        api_key=settings.dashscope_api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=temperature,
    )
