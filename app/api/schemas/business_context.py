from typing import Annotated
from uuid import UUID

from pydantic import Field

from app.domain.schemas.strict_schema import StrictSchema


class CreateBusinessContextRequest(StrictSchema):
    chunks: list[Annotated[str, Field(min_length=1)]] = Field(min_length=1)


class BusinessContextResponse(StrictSchema):
    case_snapshot_id: UUID
    chunks_added: int
