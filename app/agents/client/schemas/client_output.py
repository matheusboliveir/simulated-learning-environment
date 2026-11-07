from app.domain.schemas.strict_schema import StrictSchema


class ClientOutput(StrictSchema):
    response: str
    used_information_ids: list[str]
    additional_information_candidates: list[str]
