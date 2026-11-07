from pydantic import Field

from app.domain.enums.trust_criterion import TrustCriterion
from app.domain.schemas.strict_schema import StrictSchema


class TrustEvaluatorOutput(StrictSchema):
    trust_delta: float = Field(ge=-0.25, le=0.25)
    reason: str
    evaluated_criteria: list[TrustCriterion]
