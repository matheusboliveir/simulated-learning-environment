from pydantic import Field

from app.domain.schemas.strict_schema import StrictSchema


class SendMessageRequest(StrictSchema):
    content: str = Field(min_length=1)