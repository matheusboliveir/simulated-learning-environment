from datetime import datetime
from uuid import UUID

from app.api.schemas.orm_response import ORMResponse
from app.domain.enums.simulation_status import SimulationStatus


class SimulationResponse(ORMResponse):
    id: UUID
    user_id: UUID
    case_snapshot_id: UUID
    current_tolerance: float
    current_trust: float
    status: SimulationStatus
    created_at: datetime
