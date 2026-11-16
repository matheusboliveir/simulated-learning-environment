from typing import Annotated

from fastapi import Depends, Request
from langchain_core.embeddings import Embeddings

from app.api.dependencies.case_snapshots import get_case_snapshot_repository
from app.application.business_contexts.create_business_context import (
    CreateBusinessContext,
)
from app.infrastructure.database.repositories.case_snapshot_repository import (
    CaseSnapshotRepository,
)
from app.infrastructure.vector.repositories.business_context_repository import (
    BusinessContextRepository,
)


def get_business_context_repository(
    request: Request,
) -> BusinessContextRepository:
    return BusinessContextRepository(request.app.state.qdrant_client)


def get_embeddings(request: Request) -> Embeddings:
    return request.app.state.embeddings


def get_create_business_context(
    case_snapshot_repository: Annotated[
        CaseSnapshotRepository,
        Depends(get_case_snapshot_repository),
    ],
    business_context_repository: Annotated[
        BusinessContextRepository,
        Depends(get_business_context_repository),
    ],
    embeddings: Annotated[Embeddings, Depends(get_embeddings)],
) -> CreateBusinessContext:
    return CreateBusinessContext(
        case_snapshot_repository=case_snapshot_repository,
        business_context_repository=business_context_repository,
        embeddings=embeddings,
    )
