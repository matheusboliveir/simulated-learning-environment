from uuid import UUID

from app.domain.constants.tolerance_initial_values import TOLERANCE_INITIAL_VALUES
from app.infrastructure.database.models.simulation.simulation import SimulationModel
from app.infrastructure.database.repositories.case_snapshot_repository import (
    CaseSnapshotRepository,
)
from app.infrastructure.database.repositories.persona_snapshot_repository import (
    PersonaSnapshotRepository,
)
from app.infrastructure.database.repositories.simulation_repository import (
    SimulationRepository,
)
from app.infrastructure.database.repositories.user_repository import UserRepository


class CreateSimulation:
    def __init__(
        self,
        simulation_repository: SimulationRepository,
        user_repository: UserRepository,
        case_snapshot_repository: CaseSnapshotRepository,
        persona_snapshot_repository: PersonaSnapshotRepository,
    ) -> None:
        self._simulation_repository = simulation_repository
        self._user_repository = user_repository
        self._case_snapshot_repository = case_snapshot_repository
        self._persona_snapshot_repository = persona_snapshot_repository

    async def execute(
        self,
        *,
        user_id: UUID,
        case_snapshot_id: UUID,
    ) -> SimulationModel:
        if await self._user_repository.get_by_id(user_id) is None:
            raise LookupError("User not found.")

        case_snapshot = await self._case_snapshot_repository.get_by_id(
            case_snapshot_id
        )
        if case_snapshot is None:
            raise LookupError("Case snapshot not found.")

        persona_snapshot = await self._persona_snapshot_repository.get_by_id(
            case_snapshot.persona_snapshot_id
        )
        if persona_snapshot is None:
            raise LookupError("Persona snapshot not found.")

        return await self._simulation_repository.create(
            user_id=user_id,
            case_snapshot_id=case_snapshot_id,
            current_tolerance=TOLERANCE_INITIAL_VALUES[persona_snapshot.tolerance],
        )
