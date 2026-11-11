from qdrant_client import AsyncQdrantClient

from app.core.config import get_settings


def create_qdrant_client() -> AsyncQdrantClient:
    settings = get_settings()

    return AsyncQdrantClient(
        url=settings.qdrant_url,
        api_key=(
            settings.qdrant_api_key.get_secret_value()
            if settings.qdrant_api_key
            else None
        ),
        timeout=settings.qdrant_timeout,
    )
