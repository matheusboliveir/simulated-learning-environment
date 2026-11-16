from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.api.schemas.orm_response import ORMResponse
from app.domain.enums.tolerance_preset import TolerancePreset
from app.domain.schemas.strict_schema import StrictSchema


class CreatePersonaSnapshotRequest(StrictSchema):
    name: str = Field(min_length=1, max_length=50)
    position: str = Field(min_length=1, max_length=50)
    knowledge: list[str]
    personality: str = Field(min_length=1, max_length=255)
    communication_style: str = Field(min_length=1, max_length=100)
    tolerance: TolerancePreset = TolerancePreset.PROFESSIONAL
    background: str = Field(min_length=1)
    pain_points: list[str]
    biases: list[str]


class PersonaSnapshotResponse(ORMResponse):
    id: UUID
    name: str
    position: str
    knowledge: list[str]
    personality: str
    communication_style: str
    tolerance: TolerancePreset
    background: str
    pain_points: list[str]
    biases: list[str]
    created_at: datetime
