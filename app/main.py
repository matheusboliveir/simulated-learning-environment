from fastapi import FastAPI

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