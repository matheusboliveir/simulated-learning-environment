from pydantic import ConfigDict

from app.agents.client.schemas.states.behavioral_state import BehavioralState
from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.domain.schemas.strict_schema import StrictSchema
from app.infrastructure.database.models.simulation.persona_snapshot import (
    PersonaSnapshotModel,
)


class ClientAssessmentInput(StrictSchema):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    business_context: str
    retrieved_messages: list[SimulationMessage]
    student_message: str
    persona: PersonaSnapshotModel
    behavioral_state: BehavioralState
