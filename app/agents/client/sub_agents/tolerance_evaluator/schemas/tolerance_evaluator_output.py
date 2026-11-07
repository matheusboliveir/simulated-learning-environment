from app.domain.enums.behavior_type import BehaviorType
from app.domain.schemas.strict_schema import StrictSchema


class ToleranceEvaluatorOutput(StrictSchema):
    tolerance_delta: int
    reason: str
    evaluated_behaviors: list[BehaviorType]
