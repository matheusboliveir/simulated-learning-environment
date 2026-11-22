from langchain_ollama import OllamaEmbeddings

from app.core.config import Settings
from app.infrastructure.embeddings.config import resolve_embedding_model


def create_ollama_embeddings(
    settings: Settings,
) -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=resolve_embedding_model(settings),
        base_url=settings.ollama_base_url,
    )
