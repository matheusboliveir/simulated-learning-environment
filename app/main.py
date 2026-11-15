from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.agents.client.agent import ClientAgent
from app.core.config import get_settings
from app.infrastructure.database.connection import engine
from app.infrastructure.embeddings.factory import create_embeddings
from app.infrastructure.llm.factory import get_chat_model
from app.infrastructure.vector.client import create_qdrant_client
from app.infrastructure.vector.collections import ensure_collections


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    qdrant_client = create_qdrant_client()
    embeddings = create_embeddings()
    try:
        await ensure_collections(
            qdrant_client,
            settings.embedding_dimensions,
        )
        app.state.qdrant_client = qdrant_client
        app.state.embeddings = embeddings
        app.state.client_agent = ClientAgent(
            qdrant_client=qdrant_client,
            embeddings=embeddings
        )
        yield
    finally:
        await qdrant_client.close()
        await engine.dispose()


app = FastAPI(
    title="TCC - Simulador de Entrevistas",
    description="Ambiente de simulação de elicitação de requisitos baseado em LLMs.",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "application": "tcc-llm",
    }
