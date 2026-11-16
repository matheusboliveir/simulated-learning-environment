from app.infrastructure.database.models.simulation.case import CaseModel
from app.infrastructure.database.repositories.case_repository import CaseRepository


class CreateCase:
    def __init__(self, case_repository: CaseRepository) -> None:
        self._case_repository = case_repository

    async def execute(
        self,
        *,
        title: str,
        description: str,
        active: bool = True,
    ) -> CaseModel:
        return await self._case_repository.create(
            title=title,
            description=description,
            active=active,
        )
