from app.domain.enums.tolerance_preset import TolerancePreset
from app.infrastructure.database.models.simulation.persona_snapshot import (
    PersonaSnapshotModel,
)
from app.infrastructure.database.repositories.persona_snapshot_repository import (
    PersonaSnapshotRepository,
)


class CreatePersonaSnapshot:
    def __init__(
        self,
        persona_snapshot_repository: PersonaSnapshotRepository,
    ) -> None:
        self._persona_snapshot_repository = persona_snapshot_repository

    async def execute(
        self,
        *,
        name: str,
        position: str,
        knowledge: list[str],
        personality: str,
        communication_style: str,
        tolerance: TolerancePreset,
        background: str,
        pain_points: list[str],
        biases: list[str],
    ) -> PersonaSnapshotModel:
        return await self._persona_snapshot_repository.create(
            name=name,
            position=position,
            knowledge=knowledge,
            personality=personality,
            communication_style=communication_style,
            tolerance=tolerance,
            background=background,
            pain_points=pain_points,
            biases=biases,
        )
