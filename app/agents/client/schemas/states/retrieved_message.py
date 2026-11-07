from typing import TypedDict


class RetrievedMessage(TypedDict):
    message_id: str
    role: str
    content: str
    relevance_score: float
