from pydantic import Field

from app.domain.schemas.strict_schema import StrictSchema


class RetrievedContextChunk(StrictSchema):
    content: str
    chunk_index: int = Field(ge=0)
    score: float
