from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.cases import get_case_repository
from app.api.dependencies.persona_snapshots import (
    get_persona_snapshot_repository,
)
from app.application.case_snapshots.create_case_snapshot import CreateCaseSnapshot
from app.infrastructure.database.connection import get_db
from app.infrastructure.database.repositories.case_repository import CaseRepository
from app.infrastructure.database.repositories.case_snapshot_repository import (
    CaseSnapshotRepository,
)
from app.infrastructure.database.repositories.persona_snapshot_repository import (
    PersonaSnapshotRepository,
)


def get_case_snapshot_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> CaseSnapshotRepository:
    return CaseSnapshotRepository(session)


def get_create_case_snapshot(
    case_repository: Annotated[CaseRepository, Depends(get_case_repository)],
    persona_snapshot_repository: Annotated[
        PersonaSnapshotRepository,
        Depends(get_persona_snapshot_repository),
    ],
    case_snapshot_repository: Annotated[
        CaseSnapshotRepository,
        Depends(get_case_snapshot_repository),
    ],
) -> CreateCaseSnapshot:
    return CreateCaseSnapshot(
        case_repository=case_repository,
        persona_snapshot_repository=persona_snapshot_repository,
        case_snapshot_repository=case_snapshot_repository,
    )
