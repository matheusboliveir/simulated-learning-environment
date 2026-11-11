from qdrant_client import AsyncQdrantClient, models


async def create_payload_index(
    client: AsyncQdrantClient,
    collection_name: str,
    field_name: str,
    field_schema: models.PayloadSchemaType,
) -> None:
    await client.create_payload_index(
        collection_name=collection_name,
        field_name=field_name,
        field_schema=field_schema,
    )
