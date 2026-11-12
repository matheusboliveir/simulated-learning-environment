from langchain_ollama import OllamaEmbeddings

from app.core.config import Settings


def create_ollama_embeddings(
    settings: Settings,
) -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.embedding_model or "nomic-embed-text",
        base_url=settings.ollama_base_url,
    )
