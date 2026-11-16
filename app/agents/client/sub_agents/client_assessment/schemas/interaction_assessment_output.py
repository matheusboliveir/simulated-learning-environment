from app.agents.client.sub_agents.client_assessment.schemas.identified_behavior import (
    IdentifiedBehavior,
)
from app.domain.schemas.strict_schema import StrictSchema


class InteractionAssessmentOutput(StrictSchema):
    identified_behaviors: list[IdentifiedBehavior]
