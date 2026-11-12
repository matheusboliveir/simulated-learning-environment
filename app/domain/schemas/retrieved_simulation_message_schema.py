from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.domain.schemas.strict_schema import StrictSchema


class RetrievedSimulationMessage(StrictSchema):
    message: SimulationMessage
    score: float
