from app.infrastructure.database.models.user.user import UserModel
from app.infrastructure.database.repositories.user_repository import UserRepository


class CreateUser:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def execute(
        self,
        *,
        name: str,
        email: str,
        password: str,
    ) -> UserModel:
        return await self._user_repository.create(
            name=name,
            email=email,
            password=password,
        )
