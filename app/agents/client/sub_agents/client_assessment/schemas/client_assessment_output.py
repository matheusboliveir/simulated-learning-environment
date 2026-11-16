from app.agents.client.sub_agents.client_assessment.schemas.interaction_assessment_output import (
    InteractionAssessmentOutput,
)
from app.agents.client.sub_agents.client_assessment.schemas.tolerance_assessment_output import (
    ToleranceAssessmentOutput,
)
from app.agents.client.sub_agents.client_assessment.schemas.trust_assessment_output import (
    TrustAssessmentOutput,
)
from app.domain.schemas.strict_schema import StrictSchema


class ClientAssessmentOutput(StrictSchema):
    interaction_assessment: InteractionAssessmentOutput
    trust_assessment: TrustAssessmentOutput
    tolerance_assessment: ToleranceAssessmentOutput
