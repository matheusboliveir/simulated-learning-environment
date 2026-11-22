import asyncio
import logging
from collections.abc import Callable
from typing import Any

from langchain_core.embeddings import Embeddings
from qdrant_client import AsyncQdrantClient, models
from qdrant_client.conversions.common_types import PointId

from app.core.config import get_settings
from app.infrastructure.embeddings.config import resolve_embedding_model
from app.infrastructure.embeddings.factory import create_embeddings
from app.infrastructure.vector.client import create_qdrant_client
from app.infrastructure.vector.collections import ensure_collections
from app.infrastructure.vector.collections.business_context_chunks import (
    BUSINESS_CONTEXT_COLLECTION,
)
from app.infrastructure.vector.collections.names import (
    create_vector_collection_names,
)
from app.infrastructure.vector.collections.simulation_messages import (
    SIMULATION_MESSAGES_COLLECTION,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

ContentExtractor = Callable[[dict[str, Any]], str]


def get_content(payload: dict[str, Any]) -> str:
    content = payload.get("content")
    if not isinstance(content, str):
        raise TypeError("A Qdrant point is missing a string 'content' payload.")
    return content


async def reindex_collection(
    client: AsyncQdrantClient,
    *,
    source_collection: str,
    target_collection: str,
    embeddings: Embeddings,
    dimensions: int,
    content_extractor: ContentExtractor,
    batch_size: int = 64,
) -> int:
    if source_collection == target_collection:
        raise ValueError("Source and target collections must be different.")
    if not await client.collection_exists(source_collection):
        raise ValueError(f"Source collection '{source_collection}' does not exist.")

    offset: PointId | None = None
    total = 0
    while True:
        records, next_offset = await client.scroll(
            collection_name=source_collection,
            limit=batch_size,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        if records:
            payloads = [record.payload for record in records]
            if any(payload is None for payload in payloads):
                raise ValueError(
                    f"Collection '{source_collection}' has a point without payload."
                )
            point_payloads = [payload for payload in payloads if payload is not None]
            documents = [content_extractor(payload) for payload in point_payloads]
            vectors = await embeddings.aembed_documents(documents)
            if len(vectors) != len(records):
                raise ValueError("Embedding provider returned an unexpected vector count.")
            if any(len(vector) != dimensions for vector in vectors):
                raise ValueError(
                    f"Embedding provider returned a vector with a dimension other "
                    f"than {dimensions}."
                )

            await client.upsert(
                collection_name=target_collection,
                points=[
                    models.PointStruct(
                        id=record.id,
                        vector=vector,
                        payload=payload,
                    )
                    for record, vector, payload in zip(
                        records,
                        vectors,
                        point_payloads,
                        strict=True,
                    )
                ],
                wait=True,
            )
            total += len(records)

        if next_offset is None:
            break
        offset = next_offset

    return total


async def main() -> None:
    settings = get_settings()
    collection_names = create_vector_collection_names(settings)
    embeddings = create_embeddings()
    client = create_qdrant_client()
    try:
        await ensure_collections(
            client,
            settings.embedding_dimensions,
            collection_names,
        )
        logger.info(
            "Re-embedding with %s (%s dimensions).",
            resolve_embedding_model(settings),
            settings.embedding_dimensions,
        )
        contexts = await reindex_collection(
            client,
            source_collection=BUSINESS_CONTEXT_COLLECTION,
            target_collection=collection_names.business_context,
            embeddings=embeddings,
            dimensions=settings.embedding_dimensions,
            content_extractor=get_content,
        )
        messages = await reindex_collection(
            client,
            source_collection=SIMULATION_MESSAGES_COLLECTION,
            target_collection=collection_names.simulation_messages,
            embeddings=embeddings,
            dimensions=settings.embedding_dimensions,
            content_extractor=get_content,
        )
        logger.info("Reindexed %d context chunks and %d messages.", contexts, messages)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
