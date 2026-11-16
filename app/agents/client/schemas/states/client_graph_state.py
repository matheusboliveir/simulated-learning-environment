from typing import Required, TypedDict

from app.agents.client.schemas.states.behavioral_state import BehavioralState
from app.agents.client.sub_agents.client_assessment.schemas.interaction_assessment_output import (
    InteractionAssessmentOutput,
)
from app.agents.client.sub_agents.client_assessment.schemas.tolerance_assessment_output import (
    ToleranceAssessmentOutput,
)
from app.agents.client.sub_agents.client_assessment.schemas.trust_assessment_output import (
    TrustAssessmentOutput,
)
from app.agents.client.sub_agents.disclosure_planner.schemas.disclosure_planner_output import (
    DisclosurePlannerOutput,
)
from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.infrastructure.database.models.simulation.persona_snapshot import (
    PersonaSnapshotModel,
)


class ClientGraphState(TypedDict, total=False):
    # Identificação da execução
    simulation_id: Required[str]
    case_snapshot_id: Required[str]
    # Entrada
    student_message: Required[str]
    # Configuração do cliente
    persona: Required[PersonaSnapshotModel]
    # Estado recebido no início da interação
    behavioral_state: Required[BehavioralState]
    # Estado após aplicar os deltas desta interação
    behavioral_state_after: BehavioralState
    # Contexto recuperado
    retrieved_messages: list[SimulationMessage]
    business_context: str
    # Avaliações
    interaction_assessment: InteractionAssessmentOutput
    trust_assessment: TrustAssessmentOutput
    tolerance_assessment: ToleranceAssessmentOutput
    # Planejamento
    disclosure_plan: DisclosurePlannerOutput
    # Resultado
    client_response: str
