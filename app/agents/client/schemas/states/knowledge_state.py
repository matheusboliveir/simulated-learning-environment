from typing import TypedDict

from app.agents.client.schemas.states.additional_information import (
    AdditionalInformation,
)


class KnowledgeState(TypedDict):
    revealed_information_ids: list[str]
    additional_information: list[AdditionalInformation]
