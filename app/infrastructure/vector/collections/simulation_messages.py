from qdrant_client import AsyncQdrantClient, models

from app.infrastructure.vector.utils import create_payload_index

SIMULATION_MESSAGES_COLLECTION = "simulation_messages"


async def ensure_simulation_messages_collection(
    client: AsyncQdrantClient,
    vector_size: int,
) -> None:
    if not await client.collection_exists(SIMULATION_MESSAGES_COLLECTION):
        await client.create_collection(
            collection_name=SIMULATION_MESSAGES_COLLECTION,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    await create_payload_index(
        client,
        SIMULATION_MESSAGES_COLLECTION,
        "simulation_id",
        models.PayloadSchemaType.KEYWORD,
    )

    await create_payload_index(
        client,
        SIMULATION_MESSAGES_COLLECTION,
        "role",
        models.PayloadSchemaType.KEYWORD,
    )

    await create_payload_index(
        client,
        SIMULATION_MESSAGES_COLLECTION,
        "sequence",
        models.PayloadSchemaType.INTEGER,
    )
