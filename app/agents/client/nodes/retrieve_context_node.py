import asyncio
from uuid import UUID

from langchain_core.embeddings import Embeddings

from app.agents.client.schemas.nodes.retrieve_context_node_output import (
    RetrievedContextNodeOutput,
)
from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.infrastructure.vector.repositories.business_context_repository import (
    BusinessContextRepository,
)
from app.infrastructure.vector.repositories.simulation_message_repository import (
    SimulationMessageRepository,
)
from app.utils.timing import measure_awaitable, measure_duration


def _deduplicate_repeated_ai_messages(
    messages: list[SimulationMessage],
) -> list[SimulationMessage]:
    seen_contents: set[str] = set()
    unique_messages: list[SimulationMessage] = []

    for message in reversed(messages):
        if message.role == "ai":
            normalized_content = " ".join(message.content.casefold().split())
            if normalized_content in seen_contents:
                continue
            seen_contents.add(normalized_content)
        unique_messages.append(message)

    return list(reversed(unique_messages))


def create_retrieve_context_node(
    message_repository: SimulationMessageRepository,
    context_repository: BusinessContextRepository,
    embeddings: Embeddings,
):
    async def retrieve_context(state: ClientGraphState) -> RetrievedContextNodeOutput:
        with measure_duration("client.retrieve_context.total"):
            simulation_id = UUID(state["simulation_id"])
            latest_messages, embedding = await asyncio.gather(
                measure_awaitable(
                    "client.retrieve_context.latest_messages",
                    message_repository.get_latest_messages(
                        simulation_id=simulation_id,
                    ),
                ),
                measure_awaitable(
                    "client.retrieve_context.student_embedding",
                    embeddings.aembed_query(state["student_message"]),
                ),
            )

            before_sequence = (
                latest_messages[0].sequence if latest_messages else None
            )
            similar_messages, context_chunks = await asyncio.gather(
                measure_awaitable(
                    "client.retrieve_context.similar_messages",
                    message_repository.search_similar_messages(
                        simulation_id=simulation_id,
                        embedding=embedding,
                        before_sequence=before_sequence,
                        limit=10,
                    ),
                ),
                measure_awaitable(
                    "client.retrieve_context.business_chunks",
                    context_repository.search_similar_chunks(
                        case_snapshot_id=UUID(state["case_snapshot_id"]),
                        embedding=embedding,
                        limit=3,
                    ),
                ),
            )

            messages_by_id = {message.id: message for message in latest_messages}
            for retrieved in similar_messages:
                messages_by_id[retrieved.message.id] = retrieved.message

            retrieved_messages = sorted(
                messages_by_id.values(),
                key=lambda message: message.sequence,
            )
            retrieved_messages = _deduplicate_repeated_ai_messages(
                retrieved_messages
            )
            business_context = "\n\n".join(
                chunk.content for chunk in context_chunks
            )

            return RetrievedContextNodeOutput(
                retrieved_messages=retrieved_messages,
                business_context=business_context,
                student_message_embedding=embedding,
            )

    return retrieve_context
