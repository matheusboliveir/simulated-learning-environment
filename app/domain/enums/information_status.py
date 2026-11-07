from enum import Enum


class InformationStatus(str, Enum):
    REVEALED = "revealed"
    ACCEPTED_SUGGESTION = "accepted_suggestion"
    GENERATED = "generated"