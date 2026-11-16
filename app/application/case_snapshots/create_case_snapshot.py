from uuid import UUID

from app.infrastructure.database.models.simulation.case_snapshot import (
    CaseSnapshotModel,
)
from app.infrastructure.database.repositories.case_repository import CaseRepository
from app.infrastructure.database.repositories.case_snapshot_repository import (
    CaseSnapshotRepository,
)
from app.infrastructure.database.repositories.persona_snapshot_repository import (
    PersonaSnapshotRepository,
)


class CreateCaseSnapshot:
    def __init__(
        self,
        case_repository: CaseRepository,
        persona_snapshot_repository: PersonaSnapshotRepository,
        case_snapshot_repository: CaseSnapshotRepository,
    ) -> None:
        self._case_repository = case_repository
        self._persona_snapshot_repository = persona_snapshot_repository
        self._case_snapshot_repository = case_snapshot_repository

    async def execute(
        self,
        *,
        case_id: UUID,
        persona_snapshot_id: UUID,
        expected_requirements: list[str],
        context_snapshot_id: int,
    ) -> CaseSnapshotModel:
        if await self._case_repository.get_by_id(case_id) is None:
            raise LookupError("Case not found.")
        if (
            await self._persona_snapshot_repository.get_by_id(persona_snapshot_id)
            is None
        ):
            raise LookupError("Persona snapshot not found.")

        return await self._case_snapshot_repository.create(
            case_id=case_id,
            persona_snapshot_id=persona_snapshot_id,
            expected_requirements=expected_requirements,
            context_snapshot_id=context_snapshot_id,
        )
