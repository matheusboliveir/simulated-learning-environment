from typing import cast
from uuid import NAMESPACE_URL, UUID, uuid5

from qdrant_client import AsyncQdrantClient, models

from app.domain.schemas.retrieved_context_chunk_schema import (
    RetrievedContextChunk,
)
from app.infrastructure.vector.collections.business_context_chunks import (
    BUSINESS_CONTEXT_COLLECTION as COLLECTION_NAME,
)


class BusinessContextRepository:
    def __init__(
        self,
        client: AsyncQdrantClient,
        collection_name: str = COLLECTION_NAME,
    ) -> None:
        self._client = client
        self._collection_name = collection_name

    async def add_chunks(
        self,
        case_snapshot_id: UUID,
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
                        f"{case_snapshot_id}:{index}",
                    )
                ),
                vector=embedding,
                payload={
                    "case_snapshot_id": str(case_snapshot_id),
                    "content": content,
                    "chunk_index": index,
                },
            )
            for index, (content, embedding) in enumerate(zip(chunks, embeddings))
        ]

        if not points:
            return

        await self._client.upsert(
            collection_name=self._collection_name,
            points=points,
            wait=True,
        )

    async def search_similar_chunks(
        self,
        case_snapshot_id: UUID,
        embedding: list[float],
        limit: int = 10,
    ) -> list[RetrievedContextChunk]:
        result = await self._client.query_points(
            collection_name=self._collection_name,
            query=embedding,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="case_snapshot_id",
                        match=models.MatchValue(value=str(case_snapshot_id)),
                    )
                ]
            ),
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        chunks: list[RetrievedContextChunk] = []
        for point in result.points:
            if point.payload is None:
                continue

            chunks.append(
                RetrievedContextChunk(
                    content=point.payload["content"],
                    chunk_index=cast(int, point.payload["chunk_index"]),
                    score=point.score,
                )
            )

        return sorted(chunks, key=lambda chunk: chunk.chunk_index)

    async def delete_snapshot_chunks(
        self,
        case_snapshot_id: UUID,
    ) -> None:
        await self._client.delete(
            collection_name=self._collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="case_snapshot_id",
                            match=models.MatchValue(value=str(case_snapshot_id)),
                        )
                    ]
                )
            ),
            wait=True,
        )
