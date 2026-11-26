from pydantic import Field

from app.domain.constants.trust_ranges import TRUST_DELTA_LIMIT
from app.domain.enums.trust_criterion import TrustCriterion
from app.domain.schemas.strict_schema import StrictSchema


class TrustAssessmentOutput(StrictSchema):
    trust_delta: float = Field(ge=-TRUST_DELTA_LIMIT, le=TRUST_DELTA_LIMIT)
    reason: str
    evaluated_criteria: list[TrustCriterion]
