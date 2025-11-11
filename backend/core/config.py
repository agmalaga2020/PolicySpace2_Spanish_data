"""
Configuration management using Pydantic Settings.

Este módulo gestiona la configuración de la aplicación usando variables
de entorno y valores por defecto.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Los valores se cargan desde variables de entorno o desde .env
    """

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PolicySpace2 Spanish Data API"
    VERSION: str = "0.1.0"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8501",
    ]

    # Database
    DATABASE_PATH: str = Field(
        default="./datawarehouse.db",
        description="Path to SQLite database"
    )

    # Redis (optional)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Security
    SECRET_KEY: str = Field(
        default="changeme-in-production",
        description="Secret key for JWT encoding"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de settings
settings = Settings()
