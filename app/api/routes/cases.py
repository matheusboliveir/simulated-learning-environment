from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.cases import get_create_case
from app.api.schemas.cases import CaseResponse, CreateCaseRequest
from app.application.cases.create_case import CreateCase

router = APIRouter(prefix="/cases", tags=["Cases"])


@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_case(
    body: CreateCaseRequest,
    use_case: Annotated[CreateCase, Depends(get_create_case)],
) -> CaseResponse:
    return await use_case.execute(
        title=body.title,
        description=body.description,
        active=body.active,
    )
