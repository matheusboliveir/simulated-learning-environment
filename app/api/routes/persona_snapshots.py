from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.persona_snapshots import get_create_persona_snapshot
from app.api.schemas.persona_snapshots import (
    CreatePersonaSnapshotRequest,
    PersonaSnapshotResponse,
)
from app.application.persona_snapshots.create_persona_snapshot import (
    CreatePersonaSnapshot,
)

router = APIRouter(prefix="/persona-snapshots", tags=["Persona snapshots"])


@router.post(
    "",
    response_model=PersonaSnapshotResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_persona_snapshot(
    body: CreatePersonaSnapshotRequest,
    use_case: Annotated[
        CreatePersonaSnapshot,
        Depends(get_create_persona_snapshot),
    ],
) -> PersonaSnapshotResponse:
    return await use_case.execute(
        name=body.name,
        position=body.position,
        knowledge=body.knowledge,
        personality=body.personality,
        communication_style=body.communication_style,
        tolerance=body.tolerance,
        background=body.background,
        pain_points=body.pain_points,
        biases=body.biases,
    )
