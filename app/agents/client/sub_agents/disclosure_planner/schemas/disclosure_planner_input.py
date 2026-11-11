from app.agents.client.schemas.states.behavioral_state import BehavioralState
from app.agents.client.sub_agents.tolerance_evaluator.schemas.tolerance_evaluator_output import (
    ToleranceEvaluatorOutput,
)
from app.agents.client.sub_agents.trust_evaluator.schemas.trust_evaluator_output import (
    TrustEvaluatorOutput,
)
from app.domain.schemas.strict_schema import StrictSchema
from app.infrastructure.database.models.simulation.persona_snapshot import (
    PersonaSnapshotModel,
)
from app.infrastructure.database.models.simulation.simulation_message import (
    SimulationMessageModel,
)


class DisclosurePlannerInput(StrictSchema):
    student_message: str
    business_context: str
    persona: PersonaSnapshotModel
    behavioral_state: BehavioralState
    retrieved_messages: list[SimulationMessageModel]
    trust_assessment: TrustEvaluatorOutput
    tolerance_assessment: ToleranceEvaluatorOutput
