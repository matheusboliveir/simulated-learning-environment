from langchain_protocol import TypedDict

from app.domain.schemas.simulation_message_schema import SimulationMessage

class RetrievedContextNodeOutput(TypedDict):
    retrieved_messages: list[SimulationMessage]
    business_context: str