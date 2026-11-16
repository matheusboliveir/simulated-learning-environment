from datetime import datetime
from uuid import UUID

from app.api.schemas.orm_response import ORMResponse
from app.domain.schemas.strict_schema import StrictSchema


class CreateCaseSnapshotRequest(StrictSchema):
    case_id: UUID
    persona_snapshot_id: UUID
    expected_requirements: list[str]
    context_snapshot_id: int


class CaseSnapshotResponse(ORMResponse):
    id: UUID
    case_id: UUID
    persona_snapshot_id: UUID
    expected_requirements: list[str]
    context_snapshot_id: int
    version: int
    created_at: datetime
