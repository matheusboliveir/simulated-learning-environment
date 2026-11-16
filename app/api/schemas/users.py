from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.api.schemas.orm_response import ORMResponse
from app.domain.schemas.strict_schema import StrictSchema


class CreateUserRequest(StrictSchema):
    name: str = Field(min_length=1, max_length=30)
    email: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=8)


class UserResponse(ORMResponse):
    id: UUID
    name: str
    email: str
    created_at: datetime
