from app.domain.enums.conversation_action import ConversationAction
from app.domain.schemas.strict_schema import StrictSchema


class ConversationDirection(StrictSchema):
    action: ConversationAction
    suggested_topic: str | None = None
    reason: str
