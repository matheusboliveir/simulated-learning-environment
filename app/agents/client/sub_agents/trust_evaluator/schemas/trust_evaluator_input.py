from pydantic import Field

from app.agents.client.sub_agents.interaction_evaluator.schemas.identified_behavior import (
    IdentifiedBehavior,
)
from app.domain.schemas.strict_schema import StrictSchema
from app.infrastructure.database.models.simulation.simulation_message import SimulationMessageModel


class TrustEvaluatorInput(StrictSchema):
    student_message: str
    retrieved_messages: list[SimulationMessageModel]
    client_personality: str
    current_trust: float = Field(ge=1.0, le=5.0)
    identified_behaviors: list[IdentifiedBehavior]