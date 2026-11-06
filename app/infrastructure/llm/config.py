
from pydantic import BaseModel, ConfigDict, Field


class AgentLLMConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    model: str | None = None
    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
    )
