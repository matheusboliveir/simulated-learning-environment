from pydantic import ConfigDict

from app.agents.client.schemas.states.behavioral_state import BehavioralState
from app.agents.client.sub_agents.client_assessment.schemas.tolerance_assessment_output import (
    ToleranceAssessmentOutput,
)
from app.agents.client.sub_agents.client_assessment.schemas.trust_assessment_output import (
    TrustAssessmentOutput,
)
from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.domain.schemas.strict_schema import StrictSchema
from app.infrastructure.database.models.simulation.persona_snapshot import (
    PersonaSnapshotModel,
)


class DisclosurePlannerInput(StrictSchema):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    student_message: str
    business_context: str
    persona: PersonaSnapshotModel
    behavioral_state_before: BehavioralState
    behavioral_state_after: BehavioralState
    retrieved_messages: list[SimulationMessage]
    trust_assessment: TrustAssessmentOutput
    tolerance_assessment: ToleranceAssessmentOutput
