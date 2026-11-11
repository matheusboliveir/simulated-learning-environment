from pydantic import Field

from app.agents.client.sub_agents.interaction_evaluator.schemas.identified_behavior import (
    IdentifiedBehavior,
)
from app.domain.schemas.strict_schema import StrictSchema
from app.infrastructure.database.models.simulation.persona_snapshot import (
    PersonaSnapshotModel,
)


class ToleranceEvaluatorInput(StrictSchema):
    persona: PersonaSnapshotModel
    current_tolerance: int = Field(ge=0, le=120)
    identified_behaviors: list[IdentifiedBehavior]
