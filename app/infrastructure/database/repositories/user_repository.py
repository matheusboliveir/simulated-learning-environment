from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.user.user import UserModel
from app.infrastructure.database.repositories._utils import (
    flush_and_commit,
    validate_pagination,
)


class UserRepository:
    _updateable_fields = frozenset({"name", "email", "password"})

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        name: str,
        email: str,
        password: str,
    ) -> UserModel:
        user = UserModel(name=name, email=email)
        user.password = password
        self._session.add(user)
        await flush_and_commit(self._session)
        return user

    async def get_by_id(self, user_id: UUID) -> UserModel | None:
        return await self._session.get(UserModel, user_id)

    async def list_all(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[UserModel]:
        validate_pagination(limit, offset)
        result = await self._session.scalars(
            select(UserModel)
            .order_by(UserModel.created_at.desc(), UserModel.id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.all())

    async def update_by_id(self, user_id: UUID, **changes: object) -> UserModel | None:
        if not changes:
            raise ValueError("At least one field must be provided.")

        unsupported_fields = changes.keys() - self._updateable_fields
        if unsupported_fields:
            fields = ", ".join(sorted(unsupported_fields))
            raise ValueError(f"Unsupported user update fields: {fields}")
        for field in {"name", "email"} & changes.keys():
            if not isinstance(changes[field], str):
                raise TypeError(f"{field} must be a string.")
        if "password" in changes and not isinstance(changes["password"], str):
            raise TypeError("password must be a string.")

        user = await self.get_by_id(user_id)
        if user is None:
            return None

        for field, value in changes.items():
            if field == "password":
                if not isinstance(value, str):
                    raise TypeError("password must be a string.")
                user.password = value
            else:
                setattr(user, field, value)

        await flush_and_commit(self._session)
        return user

    async def delete_by_id(self, user_id: UUID) -> bool:
        user = await self.get_by_id(user_id)
        if user is None:
            return False

        await self._session.delete(user)
        await flush_and_commit(self._session)
        return True
