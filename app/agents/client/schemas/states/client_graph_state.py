from typing import TypedDict

from app.agents.client.schemas.client_output import ClientOutput
from app.agents.client.schemas.states.behavioral_state import BehavioralState
from app.agents.client.schemas.states.knowledge_state import KnowledgeState
from app.agents.client.schemas.states.retrieved_context import RetrievedContext
from app.agents.client.sub_agents.disclosure_planner.schemas.disclosure_planner_output import (
    DisclosurePlannerOutput,
)
from app.agents.client.sub_agents.interaction_evaluator.schemas.interaction_evaluator_output import (
    InteractionEvaluatorOutput,
)
from app.agents.client.sub_agents.tolerance_evaluator.schemas.tolerance_evaluator_output import (
    ToleranceEvaluatorOutput,
)
from app.agents.client.sub_agents.trust_evaluator.schemas.trust_evaluator_output import (
    TrustEvaluatorOutput,
)
from app.domain.enums.tolerance_preset import TolerancePreset


class ClientGraphState(TypedDict, total=False):
    # Identificação da execução
    simulation_id: str
    interaction_id: str
    # Entrada
    student_message: str
    # Configuração do cliente
    client_personality: str
    tolerance_preset: TolerancePreset
    # Estado comportamental
    behavioral_state: BehavioralState
    # Contexto recuperado
    retrieved_context: RetrievedContext
    # Conhecimento adicional
    knowledge_state: KnowledgeState
    # Avaliações
    interaction_assessment: InteractionEvaluatorOutput
    trust_assessment: TrustEvaluatorOutput
    tolerance_assessment: ToleranceEvaluatorOutput
    # Planejamento
    disclosure_plan: DisclosurePlannerOutput
    # Resultado
    client_response: ClientOutput
