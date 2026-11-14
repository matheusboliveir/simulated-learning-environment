from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.domain.schemas.strict_schema import StrictSchema


class InteractionEvaluatorInput(StrictSchema):
    student_message: str
    retrieved_messages: list[SimulationMessage]
    business_context: str
