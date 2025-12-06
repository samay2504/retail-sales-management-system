"""Application configuration using Pydantic v2 settings."""
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = Field(default="TruEstate API", description="Application name")
    app_env: str = Field(default="development", description="Environment")
    debug: bool = Field(default=True, description="Debug mode")
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    
    # Database (use PostgreSQL in production via DATABASE_URL env var)
    database_url: str = Field(
        default="sqlite+aiosqlite:///./truestate.db",
        description="Database connection URL (auto-converts postgresql:// to postgresql+asyncpg://)"
    )
    
    # Caching
    cache_backend: str = Field(default="memory", description="Cache backend: memory or redis")
    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis URL")
    cache_ttl: int = Field(default=30, description="Cache TTL in seconds")
    cache_max_size: int = Field(default=1000, description="Max cache size for memory backend")
    
    # CORS
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:4173,https://samay2504.github.io",
        description="Allowed CORS origins (comma-separated)"
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, description="Rate limit per minute")
    
    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="json", description="Log format: json or text")


# Global settings instance
settings = Settings()
