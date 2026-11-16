from uuid import UUID

from app.domain.schemas.strict_schema import StrictSchema


class CreateSimulationRequest(StrictSchema):
    user_id: UUID
    case_snapshot_id: UUID
