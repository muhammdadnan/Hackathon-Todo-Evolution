"""Configuration management for the FastAPI backend.

Loads and validates environment variables, provides configuration settings
for the application.
"""

import os
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    database_url: str = Field(
        ...,
        description="PostgreSQL database URL with asyncpg driver",
        validation_alias="DATABASE_URL",
    )

    # Authentication Configuration
    better_auth_secret: str = Field(
        ...,
        min_length=32,
        description="Shared secret for JWT token verification (must match frontend)",
        validation_alias="BETTER_AUTH_SECRET",
    )

    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm",
    )

    jwt_expiration_hours: int = Field(
        default=168,  # 7 days
        description="JWT token expiration time in hours",
    )

    # CORS Configuration
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated list of allowed CORS origins",
        validation_alias="CORS_ORIGINS",
    )

    # Server Configuration
    host: str = Field(
        default="0.0.0.0",
        description="Server host",
        validation_alias="HOST",
    )

    port: int = Field(
        default=8000,
        description="Server port",
        validation_alias="PORT",
    )

    # Environment
    environment: str = Field(
        default="development",
        description="Application environment (development, staging, production)",
        validation_alias="ENVIRONMENT",
    )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v.startswith("postgresql"):
            raise ValueError("DATABASE_URL must start with 'postgresql' or 'postgresql+asyncpg'")
        return v

    @field_validator("cors_origins")
    @classmethod
    def parse_cors_origins(cls, v: str) -> str:
        """Parse and validate CORS origins."""
        origins = [origin.strip() for origin in v.split(",")]
        if not origins:
            raise ValueError("At least one CORS origin must be specified")
        return v

    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings singleton.

    Returns:
        Settings: Application settings instance

    Raises:
        RuntimeError: If settings cannot be loaded
    """
    global settings
    if settings is None:
        try:
            settings = Settings()
        except Exception as e:
            raise RuntimeError(f"Failed to load settings: {e}") from e
    return settings
