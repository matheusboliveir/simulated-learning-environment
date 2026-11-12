from langchain_core.embeddings import Embeddings

from app.core.config import get_settings
from app.infrastructure.embeddings.providers.gemini import create_gemini_embeddings
from app.infrastructure.embeddings.providers.ollama import create_ollama_embeddings


def create_embeddings() -> Embeddings:
    settings = get_settings()

    if settings.embedding_provider == "gemini":
        return create_gemini_embeddings(settings)

    if settings.embedding_provider == "ollama":
        return create_ollama_embeddings(settings)

    raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")
