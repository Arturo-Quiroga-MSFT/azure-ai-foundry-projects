"""Configuration for AI Data Analyst Copilot"""
import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Azure AI Foundry Configuration
    azure_ai_project_endpoint: str = Field(
        default="",
        description="Azure AI Foundry project endpoint"
    )
    azure_subscription_id: str = Field(
        default="",
        description="Azure subscription ID"
    )
    azure_resource_group: str = Field(
        default="",
        description="Azure resource group name"
    )
    
    # Model Configuration
    orchestrator_model: str = Field(
        default="gpt-4o",
        description="Model for orchestrator/manager"
    )
    research_model: str = Field(
        default="gpt-4o-search-preview",
        description="Model with search capabilities for research"
    )
    coder_model: str = Field(
        default="gpt-4o",
        description="Model for code generation"
    )
    insights_model: str = Field(
        default="gpt-4o",
        description="Model for insights generation"
    )
    
    # Magentic Configuration
    max_round_count: int = Field(
        default=15,
        description="Maximum collaboration rounds"
    )
    max_stall_count: int = Field(
        default=3,
        description="Maximum rounds without progress"
    )
    max_reset_count: int = Field(
        default=2,
        description="Maximum plan resets allowed"
    )
    
    # Application Configuration
    enable_plan_review: bool = Field(
        default=False,
        description="Enable human-in-the-loop plan review"
    )
    streaming_mode: bool = Field(
        default=True,
        description="Enable streaming of agent outputs"
    )
    output_directory: Path = Field(
        default=Path("./outputs"),
        description="Directory for generated files"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    # Data Configuration
    max_data_rows: int = Field(
        default=100000,
        description="Maximum rows to load from datasets"
    )
    supported_formats: list[str] = Field(
        default=["csv", "json", "xlsx", "parquet"],
        description="Supported data file formats"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create output directory if it doesn't exist
        self.output_directory.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings


def update_settings(**kwargs) -> Settings:
    """Update settings with new values"""
    global settings
    for key, value in kwargs.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
    return settings
