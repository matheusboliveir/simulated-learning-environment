from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.api.schemas.orm_response import ORMResponse
from app.domain.schemas.strict_schema import StrictSchema


class CreateCaseRequest(StrictSchema):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=255)
    active: bool = True


class CaseResponse(ORMResponse):
    id: UUID
    title: str
    description: str
    active: bool
    created_at: datetime
