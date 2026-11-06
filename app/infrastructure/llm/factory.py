
from langchain_core.language_models.chat_models import BaseChatModel

from app.core.config import get_settings
from app.infrastructure.llm.config import AgentLLMConfig


def get_chat_model(
    agent_config: AgentLLMConfig | None = None,
) -> BaseChatModel:
    settings = get_settings()
    agent_config = agent_config or AgentLLMConfig()

    temperature = (
        agent_config.temperature
        if agent_config.temperature is not None
        else settings.llm_temperature
    )

    model = (
        agent_config.model
        or settings.llm_model
    )

    if settings.llm_provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY não foi configurada."
            )

        return ChatGoogleGenerativeAI(
            model=model or settings.gemini_model,
            google_api_key=settings.gemini_api_key.get_secret_value(),
            temperature=temperature,
            timeout=settings.llm_timeout,
        )

    if settings.llm_provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=model or settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=temperature,
        )

    raise ValueError(
        f"Provedor não suportado: {settings.llm_provider}"
    )
