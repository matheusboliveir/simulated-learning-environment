from qdrant_client import AsyncQdrantClient

from app.infrastructure.vector.collections.business_context_chunks import (
    ensure_business_context_collection,
)
from app.infrastructure.vector.collections.simulation_messages import (
    ensure_simulation_messages_collection,
)


async def ensure_collections(
    client: AsyncQdrantClient,
    vector_size: int,
) -> None:
    await ensure_simulation_messages_collection(client, vector_size)
    await ensure_business_context_collection(client, vector_size)
