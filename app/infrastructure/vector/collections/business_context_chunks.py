from qdrant_client import AsyncQdrantClient, models

from app.infrastructure.vector.utils import create_payload_index

BUSINESS_CONTEXT_COLLECTION = "business_context_chunks"


async def ensure_business_context_collection(
    client: AsyncQdrantClient,
    vector_size: int,
) -> None:
    if not await client.collection_exists(BUSINESS_CONTEXT_COLLECTION):
        await client.create_collection(
            collection_name=BUSINESS_CONTEXT_COLLECTION,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    await create_payload_index(
        client,
        BUSINESS_CONTEXT_COLLECTION,
        "context_snapshot_id",
        models.PayloadSchemaType.KEYWORD,
    )
