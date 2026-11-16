from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.cases.create_case import CreateCase
from app.infrastructure.database.connection import get_db
from app.infrastructure.database.repositories.case_repository import CaseRepository


def get_case_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> CaseRepository:
    return CaseRepository(session)


def get_create_case(
    case_repository: Annotated[CaseRepository, Depends(get_case_repository)],
) -> CreateCase:
    return CreateCase(case_repository)
