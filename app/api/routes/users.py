from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.users import get_create_user
from app.api.schemas.users import CreateUserRequest, UserResponse
from app.application.users.create_user import CreateUser

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    body: CreateUserRequest,
    use_case: Annotated[CreateUser, Depends(get_create_user)],
) -> UserResponse:
    return await use_case.execute(
        name=body.name,
        email=body.email,
        password=body.password,
    )
