from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.users.create_user import CreateUser
from app.infrastructure.database.connection import get_db
from app.infrastructure.database.repositories.user_repository import UserRepository


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    return UserRepository(session)


def get_create_user(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> CreateUser:
    return CreateUser(user_repository)
