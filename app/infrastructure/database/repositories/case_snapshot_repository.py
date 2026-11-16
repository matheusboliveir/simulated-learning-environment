from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.simulation.case import CaseModel
from app.infrastructure.database.models.simulation.case_snapshot import (
    CaseSnapshotModel,
)
from app.infrastructure.database.repositories._utils import (
    flush_and_commit,
    validate_pagination,
)


class CaseSnapshotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        case_id: UUID,
        expected_requirements: list[str],
        persona_snapshot_id: UUID,
        context_snapshot_id: int,
    ) -> CaseSnapshotModel:
        await self._session.execute(
            select(CaseModel.id)
            .where(CaseModel.id == case_id)
            .with_for_update()
        )
        latest_version = await self._session.scalar(
            select(func.max(CaseSnapshotModel.version)).where(
                CaseSnapshotModel.case_id == case_id
            )
        )
        snapshot = CaseSnapshotModel(
            case_id=case_id,
            expected_requirements=expected_requirements,
            persona_snapshot_id=persona_snapshot_id,
            context_snapshot_id=context_snapshot_id,
            version=(latest_version or 0) + 1,
        )
        self._session.add(snapshot)
        await flush_and_commit(self._session)
        return snapshot

    async def get_by_id(self, snapshot_id: UUID) -> CaseSnapshotModel | None:
        return await self._session.get(CaseSnapshotModel, snapshot_id)

    async def get_latest_by_case_id(
        self,
        case_id: UUID,
    ) -> CaseSnapshotModel | None:
        result = await self._session.scalars(
            select(CaseSnapshotModel)
            .where(CaseSnapshotModel.case_id == case_id)
            .order_by(CaseSnapshotModel.version.desc())
            .limit(1)
        )
        return result.first()

    async def list_by_case_id(
        self,
        case_id: UUID,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[CaseSnapshotModel]:
        validate_pagination(limit, offset)
        result = await self._session.scalars(
            select(CaseSnapshotModel)
            .where(CaseSnapshotModel.case_id == case_id)
            .order_by(CaseSnapshotModel.version.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.all())
