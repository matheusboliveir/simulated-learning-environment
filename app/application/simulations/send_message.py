from uuid import UUID

from app.agents.client.agent import ClientAgent
from app.agents.client.schemas.states.behavioral_state import BehavioralState
from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.infrastructure.database.repositories.simulation_repository import (
    SimulationRepository,
)


class SendMessage:
    def __init__(
        self,
        simulation_repository: SimulationRepository,
        client_agent: ClientAgent,
    ) -> None:
        self._simulation_repository = simulation_repository
        self._client_agent = client_agent

    async def execute(
        self,
        simulation_id: UUID,
        student_message: str,
    ) -> dict[str,str]:
        simulation = await self._simulation_repository.get_by_id(
            simulation_id=simulation_id,
        )

        if simulation is None:
            raise ValueError("Simulation not found.")

        initial_state = ClientGraphState(
            simulation_id=str(simulation.id),
            case_snapshot_id=str(simulation.case_snapshot_id),
            student_message=student_message,
            persona=simulation.case_snapshot.persona_snapshot,
            behavioral_state=BehavioralState(
                    trust=simulation.current_trust,
                    tolerance=simulation.current_tolerance,
                )
        )
        

        result = await self._client_agent.ainvoke(initial_state)

        return { "response": result.get("client_response", "") }