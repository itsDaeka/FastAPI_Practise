# config/settings.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # General App settings
    app_name: str = "FastAPI Practise"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug_mode: bool = True

    # Database
    database_url: str = "sqlite:///data/spendings.db"

    # Secrets / API Keys
    api_key: str = ""

    class Config:
        env_file = ".env"   # Load from .env file
        env_file_encoding = "utf-8"

# IMPORTANT: Cache so settings load only once (not every request)
@lru_cache
def get_settings() -> Settings:
    return Settings()