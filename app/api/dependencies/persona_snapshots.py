from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.persona_snapshots.create_persona_snapshot import (
    CreatePersonaSnapshot,
)
from app.infrastructure.database.connection import get_db
from app.infrastructure.database.repositories.persona_snapshot_repository import (
    PersonaSnapshotRepository,
)


def get_persona_snapshot_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> PersonaSnapshotRepository:
    return PersonaSnapshotRepository(session)


def get_create_persona_snapshot(
    repository: Annotated[
        PersonaSnapshotRepository,
        Depends(get_persona_snapshot_repository),
    ],
) -> CreatePersonaSnapshot:
    return CreatePersonaSnapshot(repository)
