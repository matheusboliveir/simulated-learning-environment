from app.agents.client.schemas.states.retrieved_context import RetrievedContext
from app.domain.schemas.strict_schema import StrictSchema


class InteractionEvaluatorInput(StrictSchema):
    student_message: str
    retrieved_context: RetrievedContext
