from app.agents.client.sub_agents.disclosure_planner.schemas.conversation_direction import (
    ConversationDirection,
)
from app.agents.client.sub_agents.disclosure_planner.schemas.information_decision import (
    InformationDecision,
)
from app.agents.client.sub_agents.disclosure_planner.schemas.new_information_candidate import (
    NewInformationCandidate,
)
from app.domain.schemas.strict_schema import StrictSchema


class DisclosurePlannerOutput(StrictSchema):
    information_decisions: list[InformationDecision]
    conversation_direction: ConversationDirection
    new_information_candidates: list[NewInformationCandidate]
