from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.simulation.case import CaseModel
from app.infrastructure.database.repositories._utils import (
    flush_and_commit,
    validate_pagination,
)


class CaseRepository:
    _updateable_fields = frozenset({"title", "description", "active"})

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        title: str,
        description: str,
        active: bool = True,
    ) -> CaseModel:
        case = CaseModel(title=title, description=description, active=active)
        self._session.add(case)
        await flush_and_commit(self._session)
        return case

    async def get_by_id(self, case_id: UUID) -> CaseModel | None:
        return await self._session.get(CaseModel, case_id)

    async def list_all(
        self,
        *,
        active: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[CaseModel]:
        validate_pagination(limit, offset)
        statement = select(CaseModel)
        if active is not None:
            statement = statement.where(CaseModel.active == active)

        result = await self._session.scalars(
            statement.order_by(CaseModel.created_at.desc(), CaseModel.id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.all())

    async def update_by_id(self, case_id: UUID, **changes: object) -> CaseModel | None:
        if not changes:
            raise ValueError("At least one field must be provided.")

        unsupported_fields = changes.keys() - self._updateable_fields
        if unsupported_fields:
            fields = ", ".join(sorted(unsupported_fields))
            raise ValueError(f"Unsupported case update fields: {fields}")
        if "title" in changes and not isinstance(changes["title"], str):
            raise TypeError("title must be a string.")
        if "description" in changes and not isinstance(changes["description"], str):
            raise TypeError("description must be a string.")
        if "active" in changes and not isinstance(changes["active"], bool):
            raise TypeError("active must be a boolean.")

        case = await self.get_by_id(case_id)
        if case is None:
            return None

        for field, value in changes.items():
            setattr(case, field, value)

        await flush_and_commit(self._session)
        return case

    async def delete_by_id(self, case_id: UUID) -> bool:
        case = await self.get_by_id(case_id)
        if case is None:
            return False

        await self._session.delete(case)
        await flush_and_commit(self._session)
        return True
