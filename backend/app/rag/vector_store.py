from langchain_community.vectorstores import Chroma

from app.core.config import settings


def get_embeddings():
    if not settings.dashscope_api_key or settings.dashscope_api_key == "请用户自行填写":
        return None
    try:
        from langchain_community.embeddings import DashScopeEmbeddings

        return DashScopeEmbeddings(model=settings.embedding_model, dashscope_api_key=settings.dashscope_api_key)
    except Exception:
        return None


def get_chroma(collection_name: str):
    embeddings = get_embeddings()
    if embeddings is None:
        return None
    return Chroma(collection_name=collection_name, embedding_function=embeddings, persist_directory=settings.chroma_persist_dir)
