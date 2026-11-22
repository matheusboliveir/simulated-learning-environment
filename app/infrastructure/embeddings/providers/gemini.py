from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import Settings
from app.infrastructure.embeddings.config import resolve_embedding_model


def create_gemini_embeddings(
    settings: Settings,
) -> GoogleGenerativeAIEmbeddings:
    if settings.gemini_api_key is None:
        raise ValueError("GEMINI_API_KEY is required for Gemini embeddings.")

    return GoogleGenerativeAIEmbeddings(
        model=resolve_embedding_model(settings),
        api_key=settings.gemini_api_key,
        output_dimensionality=settings.embedding_dimensions,
    )
