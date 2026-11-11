from uuid import UUID

from qdrant_client import AsyncQdrantClient, models

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
                    UUID(
                        bytes=__import__("hashlib")
                        .md5(f"{context_snapshot_id}:{index}".encode())
                        .digest()
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
    ) -> list[models.ScoredPoint]:
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

        return result.points

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
