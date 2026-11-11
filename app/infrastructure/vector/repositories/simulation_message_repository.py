from datetime import datetime
from uuid import UUID

from qdrant_client import AsyncQdrantClient, models

from app.infrastructure.vector.collections.simulation_messages import (
    SIMULATION_MESSAGES_COLLECTION as COLLECTION_NAME,
)


class SimulationMessageRepository:
    def __init__(self, client: AsyncQdrantClient) -> None:
        self._client = client

    async def add_message(
        self,
        message_id: UUID,
        simulation_id: UUID,
        role: str,
        content: str,
        embedding: list[float],
        sequence: int,
        created_at: datetime,
    ) -> None:
        point = models.PointStruct(
            id=str(message_id),
            vector=embedding,
            payload={
                "simulation_id": str(simulation_id),
                "role": role,
                "content": content,
                "sequence": sequence,
                "created_at": created_at.isoformat(),
            },
        )

        await self._client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point],
            wait=True,
        )

    async def get_latest_messages(
        self,
        simulation_id: UUID,
        limit: int = 5,
    ) -> list[models.Record]:
        points, _ = await self._client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="simulation_id",
                        match=models.MatchValue(value=str(simulation_id)),
                    )
                ]
            ),
            limit=limit,
            order_by=models.OrderBy(
                key="sequence",
                direction=models.Direction.DESC,
            ),
            with_payload=True,
            with_vectors=False,
        )

        # Retorna as mensagens em ordem cronológica.
        return list(reversed(points))

    async def search_similar_messages(
        self,
        simulation_id: UUID,
        embedding: list[float],
        limit: int = 5,
        before_sequence: int | None = None,
    ) -> list[models.ScoredPoint]:
        conditions = [
            models.FieldCondition(
                key="simulation_id",
                match=models.MatchValue(value=str(simulation_id)),
            )
        ]

        if before_sequence is not None:
            conditions.append(
                models.FieldCondition(
                    key="sequence",
                    range=models.Range(lt=before_sequence),
                )
            )

        result = await self._client.query_points(
            collection_name=COLLECTION_NAME,
            query=embedding,
            query_filter=models.Filter(must=conditions),
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        return result.points

    async def delete_simulation_messages(
        self,
        simulation_id: UUID,
    ) -> None:
        await self._client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="simulation_id",
                            match=models.MatchValue(value=str(simulation_id)),
                        )
                    ]
                )
            ),
            wait=True,
        )
