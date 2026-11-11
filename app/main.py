from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database.connection import engine
from app.infrastructure.vector.client import create_qdrant_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    qdrant_client = create_qdrant_client()
    app.state.qdrant_client = qdrant_client

    try:
        yield
    finally:
        await qdrant_client.close()
        await engine.dispose()


app = FastAPI(
    title="TCC - Simulador de Entrevistas",
    description="Ambiente de simulação de elicitação de requisitos baseado em LLMs.",
    version="0.1.0",
)


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "application": "tcc-llm",
    }
