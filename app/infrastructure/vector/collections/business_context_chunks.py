from qdrant_client import AsyncQdrantClient, models

from app.infrastructure.vector.utils.create_payload_index import create_payload_index

BUSINESS_CONTEXT_COLLECTION = "business_context_chunks"


async def ensure_business_context_collection(
    client: AsyncQdrantClient,
    vector_size: int,
    collection_name: str,
) -> None:
    if not await client.collection_exists(collection_name):
        await client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    await create_payload_index(
        client,
        collection_name,
        "case_snapshot_id",
        models.PayloadSchemaType.KEYWORD,
    )
