from typing import Literal

from app.domain.schemas.strict_schema import StrictSchema


class NewInformationCandidate(StrictSchema):
    related_information_id: str | None = None
    proposed_content: str
    business_plausibility: Literal["plausible", "implausible", "uncertain"]
    accepted: bool
    reason: str
