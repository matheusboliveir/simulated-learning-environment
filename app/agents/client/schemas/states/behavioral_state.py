from app.domain.schemas.strict_schema import StrictSchema


class BehavioralState(StrictSchema):
    tolerance: int
    trust: float
