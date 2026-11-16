from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.case_snapshots import get_create_case_snapshot
from app.api.schemas.case_snapshots import (
    CaseSnapshotResponse,
    CreateCaseSnapshotRequest,
)
from app.application.case_snapshots.create_case_snapshot import CreateCaseSnapshot

router = APIRouter(prefix="/case-snapshots", tags=["Case snapshots"])


@router.post(
    "",
    response_model=CaseSnapshotResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_case_snapshot(
    body: CreateCaseSnapshotRequest,
    use_case: Annotated[
        CreateCaseSnapshot,
        Depends(get_create_case_snapshot),
    ],
) -> CaseSnapshotResponse:
    try:
        return await use_case.execute(
            case_id=body.case_id,
            persona_snapshot_id=body.persona_snapshot_id,
            expected_requirements=body.expected_requirements,
            context_snapshot_id=body.context_snapshot_id,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
