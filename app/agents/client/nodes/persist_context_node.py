import asyncio
from datetime import datetime, timezone
from typing import Any
from uuid import NAMESPACE_URL, UUID, uuid5

from langchain_core.embeddings import Embeddings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.infrastructure.database.repositories.simulation_repository import (
    SimulationRepository,
)
from app.infrastructure.vector.repositories.simulation_message_repository import (
    SimulationMessageRepository,
)
from app.utils.timing import measure_awaitable, measure_duration


def create_persist_context_node(
    message_repository: SimulationMessageRepository,
    session_factory: async_sessionmaker[AsyncSession],
    embeddings: Embeddings,
):
    async def persist_context(state: ClientGraphState) -> dict[str, Any]:
        student_message_embedding = state.get("student_message_embedding")
        if student_message_embedding is None:
            raise ValueError("Student message embedding is required.")

        retrieved_messages = state.get("retrieved_messages") or []

        last_sequence = max(
            (message.sequence for message in retrieved_messages),
            default=-1,
        )

        simulation_id = UUID(state["simulation_id"])
        student_sequence = last_sequence + 1
        client_sequence = last_sequence + 2

        tolerance_assessment = state.get("tolerance_assessment")
        tolerance_delta = (
            tolerance_assessment.tolerance_delta if tolerance_assessment else 0
        )

        trust_assessment = state.get("trust_assessment")
        trust_delta = trust_assessment.trust_delta if trust_assessment else 0

        student_message = SimulationMessage(
            id=uuid5(
                NAMESPACE_URL,
                f"{simulation_id}:{student_sequence}:human",
            ),
            simulation_id=simulation_id,
            role="human",
            content=state["student_message"],
            sequence=last_sequence + 1,
            tolerance_delta=tolerance_delta,
            trust_delta=trust_delta,
            created_at=datetime.now(timezone.utc),
        )

        client_message = SimulationMessage(
            id=uuid5(
                NAMESPACE_URL,
                f"{simulation_id}:{client_sequence}:ai",
            ),
            simulation_id=simulation_id,
            role="ai",
            content=state.get("client_response", ""),
            sequence=last_sequence + 2,
            trust_delta=0,
            tolerance_delta=0,
            created_at=datetime.now(timezone.utc),
        )

        messages = [student_message, client_message]

        behavioral_state = state.get("behavioral_state")
        behavioral_state_after = state.get(
            "behavioral_state_after",
            behavioral_state,
        )
        if behavioral_state_after is None:
            raise ValueError("Behavioral state is required to persist the simulation.")

        async def persist_messages() -> None:
            client_embeddings = await measure_awaitable(
                "client.persist_context.response_embedding",
                embeddings.aembed_documents([client_message.content]),
            )
            await measure_awaitable(
                "client.persist_context.qdrant_upsert",
                message_repository.add_messages(
                    messages=messages,
                    embeddings=[student_message_embedding, *client_embeddings],
                ),
            )

        async def update_simulation() -> None:
            async with session_factory() as session:
                simulation_repository = SimulationRepository(session)
                updated_simulation = await measure_awaitable(
                    "client.persist_context.simulation_update",
                    simulation_repository.update_by_id(
                        simulation_id=simulation_id,
                        current_tolerance=behavioral_state_after.tolerance,
                        current_trust=behavioral_state_after.trust,
                    ),
                )
            if updated_simulation is None:
                raise LookupError(f"Simulation {simulation_id} was not found.")

        with measure_duration("client.persist_context.total"):
            await asyncio.gather(persist_messages(), update_simulation())

        return {}

    return persist_context
