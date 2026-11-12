from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import Settings


def create_gemini_embeddings(
    settings: Settings,
) -> GoogleGenerativeAIEmbeddings:
    if settings.gemini_api_key is None:
        raise ValueError("GEMINI_API_KEY is required for Gemini embeddings.")

    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model or "models/gemini-embedding-001",
        google_api_key=settings.gemini_api_key.get_secret_value(),
        output_dimensionality=settings.embedding_dimensions,
    )
