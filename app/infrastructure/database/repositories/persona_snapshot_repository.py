from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums.tolerance_preset import TolerancePreset
from app.infrastructure.database.models.simulation.case_snapshot import (
    CaseSnapshotModel,
)
from app.infrastructure.database.models.simulation.persona_snapshot import (
    PersonaSnapshotModel,
)
from app.infrastructure.database.repositories._utils import (
    flush_and_commit,
    validate_pagination,
)


class PersonaSnapshotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
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
        snapshot = PersonaSnapshotModel(
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
        self._session.add(snapshot)
        await flush_and_commit(self._session)
        return snapshot

    async def get_by_id(self, snapshot_id: UUID) -> PersonaSnapshotModel | None:
        return await self._session.get(PersonaSnapshotModel, snapshot_id)

    async def list_by_case_id(
        self,
        case_id: UUID,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[PersonaSnapshotModel]:
        validate_pagination(limit, offset)
        result = await self._session.scalars(
            select(PersonaSnapshotModel)
            .join(
                CaseSnapshotModel,
                CaseSnapshotModel.persona_snapshot_id == PersonaSnapshotModel.id,
            )
            .where(CaseSnapshotModel.case_id == case_id)
            .distinct()
            .order_by(PersonaSnapshotModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.all())
