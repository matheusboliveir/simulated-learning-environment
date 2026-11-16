from uuid import UUID

from langchain_core.embeddings import Embeddings

from app.infrastructure.database.repositories.case_snapshot_repository import (
    CaseSnapshotRepository,
)
from app.infrastructure.vector.repositories.business_context_repository import (
    BusinessContextRepository,
)


class CreateBusinessContext:
    def __init__(
        self,
        case_snapshot_repository: CaseSnapshotRepository,
        business_context_repository: BusinessContextRepository,
        embeddings: Embeddings,
    ) -> None:
        self._case_snapshot_repository = case_snapshot_repository
        self._business_context_repository = business_context_repository
        self._embeddings = embeddings

    async def execute(
        self,
        *,
        case_snapshot_id: UUID,
        chunks: list[str],
    ) -> int:
        if await self._case_snapshot_repository.get_by_id(case_snapshot_id) is None:
            raise LookupError("Case snapshot not found.")

        vectors = await self._embeddings.aembed_documents(chunks)
        await self._business_context_repository.add_chunks(
            case_snapshot_id=case_snapshot_id,
            chunks=chunks,
            embeddings=vectors,
        )
        return len(chunks)
