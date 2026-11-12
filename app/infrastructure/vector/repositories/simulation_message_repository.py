from uuid import UUID

from qdrant_client import AsyncQdrantClient, models

from app.domain.schemas.retrieved_simulation_message_schema import (
    RetrievedSimulationMessage,
)
from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.infrastructure.vector.collections.simulation_messages import (
    SIMULATION_MESSAGES_COLLECTION as COLLECTION_NAME,
)


class SimulationMessageRepository:
    def __init__(self, client: AsyncQdrantClient) -> None:
        self._client = client

    async def add_message(
        self,
        message: SimulationMessage,
        embedding: list[float],
    ) -> None:
        point = models.PointStruct(
            id=str(message.id),
            vector=embedding,
            payload=message.model_dump(mode="json"),
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
    ) -> list[SimulationMessage]:
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
        return [
            SimulationMessage.model_validate(point.payload)
            for point in reversed(points)
        ]

    async def search_similar_messages(
        self,
        simulation_id: UUID,
        embedding: list[float],
        limit: int = 10,
        before_sequence: int | None = None,
    ) -> list[RetrievedSimulationMessage]:
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

        return sorted(
            [
                RetrievedSimulationMessage(
                    message=SimulationMessage.model_validate(point.payload),
                    score=point.score,
                )
                for point in result.points
            ],
            key=lambda item: item.message.sequence,
        )

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
