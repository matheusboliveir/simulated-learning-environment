from uuid import uuid4

import pytest
from qdrant_client import models

from app.core.config import get_settings
from app.infrastructure.embeddings.factory import create_embeddings
from app.infrastructure.vector.client import create_qdrant_client
from app.infrastructure.vector.collections import ensure_collections


@pytest.mark.asyncio
async def test_gemini_embeddings_with_qdrant():
    settings = get_settings()

    qdrant_client = create_qdrant_client()
    embeddings = create_embeddings()

    point_id = str(uuid4())
    simulation_id = str(uuid4())

    try:
        # Generate embedding using Gemini
        vector = await embeddings.aembed_query(
            "The system must allow users to register."
        )

        assert len(vector) == settings.embedding_dimensions

        # Ensure Qdrant collections exist
        await ensure_collections(
            qdrant_client,
            len(vector),
        )

        # Insert a test point
        await qdrant_client.upsert(
            collection_name="simulation_messages",
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "simulation_id": simulation_id,
                        "role": "student",
                        "content": "The system must allow users to register.",
                        "sequence": 1,
                    },
                )
            ],
            wait=True,
        )

        # Search using the same embedding
        result = await qdrant_client.query_points(
            collection_name="simulation_messages",
            query=vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="simulation_id",
                        match=models.MatchValue(value=simulation_id),
                    )
                ]
            ),
            limit=1,
            with_payload=True,
        )

        assert len(result.points) == 1
        assert str(result.points[0].id) == point_id

    finally:
        # Remove the test point
        await qdrant_client.delete(
            collection_name="simulation_messages",
            points_selector=models.PointIdsList(points=[point_id]),
            wait=True,
        )

        await qdrant_client.close()