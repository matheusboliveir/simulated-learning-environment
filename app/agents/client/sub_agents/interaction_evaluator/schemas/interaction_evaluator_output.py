from app.agents.client.sub_agents.interaction_evaluator.schemas.identified_behavior import (
    IdentifiedBehavior,
)
from app.domain.schemas.strict_schema import StrictSchema


class InteractionEvaluatorOutput(StrictSchema):
    identified_behaviors: list[IdentifiedBehavior]
