from app.domain.enums.behavior_type import BehaviorType
from app.domain.schemas.strict_schema import StrictSchema


class IdentifiedBehavior(StrictSchema):
    behavior: BehaviorType
    evidence: str
    confidence_relevant: bool
