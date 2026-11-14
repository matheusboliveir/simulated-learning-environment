from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    # DataBase
    database_url: str = ""

    # Provider
    llm_provider: Literal["gemini", "ollama"] = "gemini"

    # General settings
    llm_temperature: float = 0.7
    llm_timeout: int = 120

    # Gemini
    gemini_api_key: SecretStr | None = None
    gemini_model: str = "gemini-2.5-flash"

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3"

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: SecretStr | None = None
    qdrant_timeout: int = 30

    # Embeddings
    embedding_provider: Literal["gemini", "ollama"] = "gemini"
    embedding_model: str | None = None
    embedding_dimensions: int = 768


@lru_cache
def get_settings() -> Settings:
    return Settings()
