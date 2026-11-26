from app.agents.client.sub_agents.client_assessment.schemas.interaction_assessment_output import (
    InteractionAssessmentOutput,
)
from app.domain.enums.trust_criterion import TrustCriterion
from app.domain.schemas.strict_schema import StrictSchema


class ClientAssessmentLLMOutput(StrictSchema):
    """Saída pedida ao LLM. As variações numéricas não vêm do modelo:
    a aplicação as calcula a partir dos comportamentos e intensidades."""

    message_understood: bool
    interaction_assessment: InteractionAssessmentOutput
    trust_reason: str
    trust_criteria: list[TrustCriterion]
    tolerance_reason: str
