from uuid import NAMESPACE_URL, UUID, uuid5

from qdrant_client import AsyncQdrantClient, models

from app.domain.schemas.retrieved_context_chunk_schema import (
    RetrievedContextChunk,
)
from app.infrastructure.vector.collections.business_context_chunks import (
    BUSINESS_CONTEXT_COLLECTION as COLLECTION_NAME,
)


class BusinessContextRepository:
    def __init__(self, client: AsyncQdrantClient) -> None:
        self._client = client

    async def add_chunks(
        self,
        context_snapshot_id: UUID,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "The number of chunks must match the number of embeddings."
            )

        points = [
            models.PointStruct(
                id=str(
                    uuid5(
                        NAMESPACE_URL,
                        f"{context_snapshot_id}:{index}",
                    )
                ),
                vector=embedding,
                payload={
                    "context_snapshot_id": str(context_snapshot_id),
                    "content": content,
                    "chunk_index": index,
                },
            )
            for index, (content, embedding) in enumerate(zip(chunks, embeddings))
        ]

        if not points:
            return

        await self._client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
            wait=True,
        )

    async def search_similar_chunks(
        self,
        context_snapshot_id: UUID,
        embedding: list[float],
        limit: int = 5,
    ) -> list[RetrievedContextChunk]:
        result = await self._client.query_points(
            collection_name=COLLECTION_NAME,
            query=embedding,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="context_snapshot_id",
                        match=models.MatchValue(value=str(context_snapshot_id)),
                    )
                ]
            ),
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        chunks = [
            RetrievedContextChunk(
                content=point.payload["content"],
                chunk_index=point.payload["chunk_index"],
                score=point.score,
            )
            for point in result.points
        ]

        return sorted(chunks, key=lambda chunk: chunk.chunk_index)

    async def delete_snapshot_chunks(
        self,
        context_snapshot_id: UUID,
    ) -> None:
        await self._client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="context_snapshot_id",
                            match=models.MatchValue(value=str(context_snapshot_id)),
                        )
                    ]
                )
            ),
            wait=True,
        )
