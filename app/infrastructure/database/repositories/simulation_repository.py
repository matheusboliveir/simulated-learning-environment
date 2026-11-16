from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.enums.simulation_status import SimulationStatus
from app.infrastructure.database.models.simulation.case_snapshot import (
    CaseSnapshotModel,
)
from app.infrastructure.database.models.simulation.simulation import SimulationModel
from app.infrastructure.database.repositories._utils import (
    flush_and_commit,
    validate_pagination,
)


class SimulationRepository:
    _updateable_fields = frozenset(
        {"current_tolerance", "current_trust", "status"}
    )

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: UUID,
        case_snapshot_id: UUID,
        current_tolerance: float,
        current_trust: float = 1.0,
        status: SimulationStatus = SimulationStatus.CREATED,
    ) -> SimulationModel:
        simulation = SimulationModel(
            user_id=user_id,
            case_snapshot_id=case_snapshot_id,
            current_tolerance=current_tolerance,
            current_trust=current_trust,
            status=status,
        )
        self._session.add(simulation)
        await flush_and_commit(self._session)
        return simulation

    async def get_by_id(self, simulation_id: UUID) -> SimulationModel | None:
        result = await self._session.scalars(
            select(SimulationModel)
            .where(SimulationModel.id == simulation_id)
            .options(
                selectinload(SimulationModel.case_snapshot).selectinload(
                    CaseSnapshotModel.persona_snapshot
                )
            )
        )
        return result.first()

    async def list_by_user_id(
        self,
        user_id: UUID,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[SimulationModel]:
        validate_pagination(limit, offset)
        result = await self._session.scalars(
            select(SimulationModel)
            .where(SimulationModel.user_id == user_id)
            .order_by(SimulationModel.created_at.desc(), SimulationModel.id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.all())

    async def update_by_id(
        self,
        simulation_id: UUID,
        **changes: object,
    ) -> SimulationModel | None:
        if not changes:
            raise ValueError("At least one field must be provided.")

        unsupported_fields = changes.keys() - self._updateable_fields
        if unsupported_fields:
            fields = ", ".join(sorted(unsupported_fields))
            raise ValueError(f"Unsupported simulation update fields: {fields}")

        simulation = await self.get_by_id(simulation_id)
        if simulation is None:
            return None

        for field, value in changes.items():
            if field in {"current_tolerance", "current_trust"}:
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise TypeError(f"{field} must be a number.")
                value = float(value)
            elif field == "status":
                try:
                    value = SimulationStatus(value)
                except (TypeError, ValueError) as error:
                    raise ValueError("status must be a valid SimulationStatus.") from error
            setattr(simulation, field, value)

        await flush_and_commit(self._session)
        return simulation

    async def delete_by_id(self, simulation_id: UUID) -> bool:
        simulation = await self.get_by_id(simulation_id)
        if simulation is None:
            return False

        await self._session.delete(simulation)
        await flush_and_commit(self._session)
        return True