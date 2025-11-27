"""
Configuration management using pydantic-settings.
Loads configuration from environment variables with validation.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4o"
    AZURE_OPENAI_API_VERSION: str = "2024-08-01-preview"
    
    # Azure AI Foundry (optional)
    AZURE_AI_PROJECT_ENDPOINT: str = ""
    AZURE_AI_FOUNDRY_AGENT_ID: str = ""
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8888
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080"
    ]
    
    # Feature Flags
    ENABLE_STATE_MANAGEMENT: bool = True
    ENABLE_APPROVAL_WORKFLOWS: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Settings are loaded once and cached for the application lifetime.
    """
    return Settings()
