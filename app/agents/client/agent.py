from typing import cast

from langchain.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langgraph.graph import END, START, StateGraph
from qdrant_client import AsyncQdrantClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.agents.client.nodes.apply_behavioral_deltas_node import (
    create_apply_behavioral_deltas_node,
)
from app.agents.client.nodes.disclosure_planner_node import (
    create_disclosure_planner_node,
)
from app.agents.client.nodes.interaction_evaluator_node import (
    create_interaction_evaluator_node,
)
from app.agents.client.nodes.persist_context_node import create_persist_context_node
from app.agents.client.nodes.retrieve_context_node import create_retrieve_context_node
from app.agents.client.nodes.tolerance_evaluator_node import (
    create_tolerance_evaluator_node,
)
from app.agents.client.nodes.trust_evaluator_node import create_trust_evaluator_node
from app.agents.client.prompt import CLIENT_HUMAN_PROMPT, CLIENT_SYSTEM_PROMPT
from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.infrastructure.llm.factory import get_chat_model
from app.infrastructure.vector.repositories.business_context_repository import (
    BusinessContextRepository,
)
from app.infrastructure.vector.repositories.simulation_message_repository import (
    SimulationMessageRepository,
)
from app.utils.formatter import (
    format_persona_snapshot,
    format_retrieved_messages,
    format_schema,
    format_untrusted_text,
)


class ClientAgent:
    def __init__(
        self, 
        qdrant_client: AsyncQdrantClient, 
        embeddings: Embeddings,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._message_repository = SimulationMessageRepository(qdrant_client)
        self._context_repository = BusinessContextRepository(qdrant_client)
        self._session_factory = session_factory
        self._llm = get_chat_model()
        self._embeddings = embeddings
        self._graph = self._build_graph()
        self._prompt = ChatPromptTemplate.from_messages(
            [
                ("system", CLIENT_SYSTEM_PROMPT),
                ("human", CLIENT_HUMAN_PROMPT),
            ]
        )
        self._chain = self._prompt | self._llm

    def _build_graph(self):
        builder = StateGraph(ClientGraphState)

        # Instancias
        retrieve_context_node = create_retrieve_context_node(
            message_repository=self._message_repository,
            context_repository=self._context_repository,
            embeddings=self._embeddings,
        )
        interaction_evaluator_node = create_interaction_evaluator_node(llm=self._llm)
        trust_evaluator_node = create_trust_evaluator_node(llm=self._llm)
        tolerance_evaluator_node = create_tolerance_evaluator_node(llm=self._llm)
        apply_behavioral_deltas_node = create_apply_behavioral_deltas_node()
        disclosure_planner_node = create_disclosure_planner_node(llm=self._llm)
        persist_context_node = create_persist_context_node(
            message_repository=self._message_repository,
            session_factory=self._session_factory,
            embeddings=self._embeddings,
        )
        
        # Nodes
        builder.add_node("retrieve_context", retrieve_context_node)
        builder.add_node("interaction_evaluator",interaction_evaluator_node)
        builder.add_node("trust_evaluator",trust_evaluator_node)
        builder.add_node("tolerance_evaluator",tolerance_evaluator_node)
        builder.add_node("apply_behavioral_deltas", apply_behavioral_deltas_node)
        builder.add_node("disclosure_planner",disclosure_planner_node)
        builder.add_node("client_agent",self._evaluate)
        builder.add_node("persist_context", persist_context_node)
        # Edges
        builder.add_edge(START, "retrieve_context")
        builder.add_edge("retrieve_context", "interaction_evaluator")
        builder.add_edge("interaction_evaluator", "trust_evaluator")
        builder.add_edge("interaction_evaluator", "tolerance_evaluator")
        builder.add_edge(
            ["trust_evaluator", "tolerance_evaluator"],
            "apply_behavioral_deltas",
        )
        builder.add_edge("apply_behavioral_deltas", "disclosure_planner")
        builder.add_edge("disclosure_planner","client_agent")
        builder.add_edge("client_agent", "persist_context")
        builder.add_edge("persist_context", END)

        return builder.compile()
    
    async def _evaluate(self, state: ClientGraphState) -> dict[str,str]:
        behavioral_state_after = state.get("behavioral_state_after")
        if behavioral_state_after is None:
            raise ValueError("Post-interaction behavioral state is required.")

        retrieved_messages = state.get("retrieved_messages") or []
        result = await self._chain.ainvoke(
            {
                "persona": format_persona_snapshot(state["persona"]),
                "business_context": format_untrusted_text(state.get("business_context")),
                "behavioral_state_before": format_schema(state["behavioral_state"]),
                "behavioral_state_after": format_schema(behavioral_state_after),
                "interaction_assessment": format_schema(state.get("interaction_assessment")),
                "trust_assessment": format_schema(state.get("trust_assessment")),
                "tolerance_assessment": format_schema(state.get("tolerance_assessment")),
                "retrieved_messages": format_retrieved_messages(retrieved_messages),
                "disclosure_plan": format_schema(state.get("disclosure_plan")),
                "student_message": format_untrusted_text(state["student_message"]),
            }
        )
        if not isinstance(result.content, str):
            raise TypeError("The client response must be a string.")
        return { "client_response": result.content }
    
    async def ainvoke(self, state: ClientGraphState) -> ClientGraphState:
        graph = cast(Runnable[ClientGraphState, ClientGraphState], self._graph)
        return await graph.ainvoke(state)