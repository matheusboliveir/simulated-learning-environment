from pydantic import ConfigDict

from app.domain.schemas.strict_schema import StrictSchema


class ORMResponse(StrictSchema):
    model_config = ConfigDict(extra="forbid", from_attributes=True)
