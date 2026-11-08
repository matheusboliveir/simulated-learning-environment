from pydantic import Field

from app.agents.client.sub_agents.interaction_evaluator.schemas.identified_behavior import (
    IdentifiedBehavior,
)
from app.domain.enums.tolerance_preset import TolerancePreset
from app.domain.schemas.strict_schema import StrictSchema


class ToleranceEvaluatorInput(StrictSchema):
    client_personality: str
    tolerance_preset: TolerancePreset
    current_tolerance: int = Field(ge=0, le=120)
    identified_behaviors: list[IdentifiedBehavior]
