from enum import Enum


class ConversationAction(str, Enum):
    CONTINUE = "continue"
    REDIRECT = "redirect"
    DECLINE = "decline"