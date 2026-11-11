from typing import List

from app.domain.schemas.strict_schema import StrictSchema
from app.infrastructure.database.models.simulation.simulation_message import SimulationMessageModel


class InteractionEvaluatorInput(StrictSchema):
    student_message: str
    retrieved_messages: List[SimulationMessageModel]
    business_context: str
