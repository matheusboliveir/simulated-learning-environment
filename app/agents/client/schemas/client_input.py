from app.agents.client.schemas.states.behavioral_state import BehavioralState
from app.agents.client.sub_agents.disclosure_planner.schemas.disclosure_planner_output import (
    DisclosurePlannerOutput,
)
from app.agents.client.sub_agents.tolerance_evaluator.schemas.tolerance_evaluator_output import (
    ToleranceEvaluatorOutput,
)
from app.agents.client.sub_agents.trust_evaluator.schemas.trust_evaluator_output import (
    TrustEvaluatorOutput,
)
from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.domain.schemas.strict_schema import StrictSchema
from app.infrastructure.database.models.simulation.persona_snapshot import (
    PersonaSnapshotModel,
)


class ResponseGeneratorInput(StrictSchema):
    student_message: str
    persona: PersonaSnapshotModel
    behavioral_state: BehavioralState
    trust_assessment: TrustEvaluatorOutput
    tolerance_assessment: ToleranceEvaluatorOutput
    relevant_messages: list[SimulationMessage]
    disclosure_plan: DisclosurePlannerOutput
