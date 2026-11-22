from qdrant_client import AsyncQdrantClient, models

from app.infrastructure.vector.utils.create_payload_index import create_payload_index

SIMULATION_MESSAGES_COLLECTION = "simulation_messages"


async def ensure_simulation_messages_collection(
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
        "simulation_id",
        models.PayloadSchemaType.KEYWORD,
    )

    await create_payload_index(
        client,
        collection_name,
        "role",
        models.PayloadSchemaType.KEYWORD,
    )

    await create_payload_index(
        client,
        collection_name,
        "sequence",
        models.PayloadSchemaType.INTEGER,
    )
