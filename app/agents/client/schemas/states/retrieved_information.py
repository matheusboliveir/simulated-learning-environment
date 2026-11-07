from typing import TypedDict


class RetrievedInformation(TypedDict):
    information_id: str
    title: str
    trust_level: int
    content: str
    relevance_score: float
