from app.domain.enums.behavior_intensity import BehaviorIntensity
from app.domain.enums.behavior_type import BehaviorType
from app.domain.schemas.strict_schema import StrictSchema


class IdentifiedBehavior(StrictSchema):
    behavior: BehaviorType
    intensity: BehaviorIntensity
    evidence: str
