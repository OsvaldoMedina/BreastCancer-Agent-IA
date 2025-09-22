# app/config.py
from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    ENV: str = Field("dev", description="Environment name")
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key")
    OPENAI_MODEL: str = Field("gpt-4o-mini", description="LLM model name")

    # MLflow
    MLFLOW_TRACKING_URI: str = Field("http://mlflow:5000", description="MLflow tracking URI")
    MLFLOW_EXPERIMENT: str = Field("bc_assistant", description="Experiment name")

    # RAG-lite
    KNOWLEDGE_DIR: str = Field("data/knowledge", description="Local knowledge dir")
    MAX_CONTEXT_DOCS: int = Field(3, description="Max docs to stuff into context")

    # Safety
    MAX_TOKENS: int = 800
    TEMPERATURE: float = 0.2

    # API
    API_KEY: Optional[str] = Field(None, description="Static API key to protect /chat")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
