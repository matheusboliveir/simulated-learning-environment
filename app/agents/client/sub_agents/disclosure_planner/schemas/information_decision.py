from app.domain.enums.information_disclosure import InformationDisclosure
from app.domain.schemas.strict_schema import StrictSchema


class InformationDecision(StrictSchema):
    disclosure: InformationDisclosure
    content_to_communicate: str
    reason: str
