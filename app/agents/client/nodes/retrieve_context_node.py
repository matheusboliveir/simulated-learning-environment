
from uuid import UUID

from langchain_core.embeddings import Embeddings


from app.agents.client.schemas.nodes.retrieve_context_node_output import RetrievedContextNodeOutput
from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.infrastructure.vector.repositories.business_context_repository import BusinessContextRepository
from app.infrastructure.vector.repositories.simulation_message_repository import SimulationMessageRepository



def create_retrieve_context_node(
    message_repository: SimulationMessageRepository,
    context_repository: BusinessContextRepository,
    embeddings: Embeddings,
):

    async def retrieve_context(state: ClientGraphState) -> RetrievedContextNodeOutput:
      simulation_id = UUID(state["simulation_id"])
      # 1. Recupera as mensagens mais recentes.
      latest_messages = await message_repository.get_latest_messages(
					simulation_id=simulation_id
			)
      # 2. Gera o embedding da mensagem atual.
      embedding = await embeddings.aembed_query(
					state["student_message"]
			)
      # 3. Busca mensagens anteriores semanticamente relevantes.
      before_sequence = (
					latest_messages[0].sequence
					if latest_messages
					else None
			)

      similar_messages = await message_repository.search_similar_messages(
            simulation_id=simulation_id,
            embedding=embedding,
            before_sequence=before_sequence,
      )
      # 4. Combina os resultados em ordem cronológica.
      messages_by_id = {
            message.id: message
            for message in latest_messages
        }

      for retrieved in similar_messages:
            messages_by_id[retrieved.message.id] = retrieved.message

      retrieved_messages = sorted(
            messages_by_id.values(),
            key=lambda message: message.sequence,
        )

      # 5. Recupera os chunks relevantes do contexto empresarial.
      context_chunks = await context_repository.search_similar_chunks(
            case_snapshot_id=UUID(state["case_snapshot_id"]),
            embedding=embedding,
            limit=5,
        )

      business_context = "\n\n".join(
            chunk.content for chunk in context_chunks
      )

      return RetrievedContextNodeOutput(
        messages=retrieved_messages,
        context=business_context,
      )

    return retrieve_context
