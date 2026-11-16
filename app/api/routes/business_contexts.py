from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.business_context import get_create_business_context
from app.api.schemas.business_context import (
    BusinessContextResponse,
    CreateBusinessContextRequest,
)
from app.application.business_contexts.create_business_context import (
    CreateBusinessContext,
)

router = APIRouter(prefix="/case-snapshots", tags=["Business context"])


@router.post(
    "/{case_snapshot_id}/business-context",
    response_model=BusinessContextResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_business_context(
    case_snapshot_id: UUID,
    body: CreateBusinessContextRequest,
    use_case: Annotated[
        CreateBusinessContext,
        Depends(get_create_business_context),
    ],
) -> BusinessContextResponse:
    try:
        chunks_added = await use_case.execute(
            case_snapshot_id=case_snapshot_id,
            chunks=body.chunks,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return BusinessContextResponse(
        case_snapshot_id=case_snapshot_id,
        chunks_added=chunks_added,
    )
