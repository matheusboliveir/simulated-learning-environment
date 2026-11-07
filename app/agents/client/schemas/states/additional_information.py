from typing import TypedDict


class AdditionalInformation(TypedDict):
    id: str
    content: str
    related_information_id: str | None
    source: str
    status: str
