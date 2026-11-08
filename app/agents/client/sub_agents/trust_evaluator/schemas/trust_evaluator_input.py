from pydantic import Field

from app.agents.client.schemas.states.retrieved_message import RetrievedMessage
from app.agents.client.sub_agents.interaction_evaluator.schemas.identified_behavior import (
    IdentifiedBehavior,
)
from app.domain.schemas.strict_schema import StrictSchema


class TrustEvaluatorInput(StrictSchema):
    student_message: str
    retrieved_messages: list[RetrievedMessage]
    client_personality: str
    current_trust: float = Field(ge=1.0, le=5.0)
    identified_behaviors: list[IdentifiedBehavior]
