from app.domain.schemas.strict_schema import StrictSchema


class BehavioralState(StrictSchema):
    tolerance: float
    trust: float
