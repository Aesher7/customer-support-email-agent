"""Application configuration and settings."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4"

    # Email Configuration
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""

    # LangChain Configuration
    langchain_api_key: str = ""
    langchain_tracing_v2: bool = False

    # Database Configuration
    database_url: str = "sqlite:///./customer_support.db"

    # Logging Configuration
    log_level: str = "INFO"

    class Config:
        """Pydantic settings config."""
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
