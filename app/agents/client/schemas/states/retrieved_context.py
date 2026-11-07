from typing import TypedDict

from app.agents.client.schemas.states.retrieved_information import RetrievedInformation
from app.agents.client.schemas.states.retrieved_message import RetrievedMessage


class RetrievedContext(TypedDict):
    relevant_messages: list[RetrievedMessage]
    relevant_information: list[RetrievedInformation]
