from langchain_protocol import TypedDict

from app.domain.schemas.simulation_message_schema import SimulationMessage

class RetrievedContextNodeOutput(TypedDict):
    messages: list[SimulationMessage]
    context: str