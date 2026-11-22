from app.core.config import Settings


def resolve_embedding_model(settings: Settings) -> str:
    if settings.embedding_model:
        return settings.embedding_model
    if settings.embedding_provider == "gemini":
        return "models/gemini-embedding-001"
    return "embeddinggemma"