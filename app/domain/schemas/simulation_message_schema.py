from datetime import datetime
from uuid import UUID

from langchain_protocol import MessageRole
from pydantic import Field

from app.domain.schemas.strict_schema import StrictSchema


class SimulationMessage(StrictSchema):
    id: UUID
    simulation_id: UUID
    role: MessageRole
    content: str
    sequence: int = Field(ge=0)
    tolerance_delta: float | None
    trust_delta: float | None
    created_at: datetime
