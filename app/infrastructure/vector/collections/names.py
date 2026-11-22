import re
from dataclasses import dataclass

from app.core.config import Settings
from app.infrastructure.embeddings.config import resolve_embedding_model
from app.infrastructure.vector.collections.business_context_chunks import (
    BUSINESS_CONTEXT_COLLECTION,
)
from app.infrastructure.vector.collections.simulation_messages import (
    SIMULATION_MESSAGES_COLLECTION,
)


@dataclass(frozen=True)
class VectorCollectionNames:
    business_context: str
    simulation_messages: str


def create_vector_collection_names(settings: Settings) -> VectorCollectionNames:
    embedding_model = resolve_embedding_model(settings)
    if (
        settings.embedding_provider == "gemini"
        and embedding_model == "models/gemini-embedding-001"
        and settings.embedding_dimensions == 768
    ):
        return VectorCollectionNames(
            business_context=BUSINESS_CONTEXT_COLLECTION,
            simulation_messages=SIMULATION_MESSAGES_COLLECTION,
        )

    model_name = re.sub(r"[^a-z0-9]+", "_", embedding_model.lower()).strip("_")
    suffix = (
        f"{settings.embedding_provider}__{model_name}"
        f"__{settings.embedding_dimensions}"
    )
    return VectorCollectionNames(
        business_context=f"{BUSINESS_CONTEXT_COLLECTION}__{suffix}",
        simulation_messages=f"{SIMULATION_MESSAGES_COLLECTION}__{suffix}",
    )
