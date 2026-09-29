from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "FitBuddy - AI Fitness Plan Generator"
    database_url: str = "sqlite:///./fitbuddy.db"
    gemini_api_key: str = ""
    workout_model: str = "gemini-3.8-flash"
    nutrition_model: str = "gemini-3.8-flash"
    admin_key: str = "fitbuddy-admin-123"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()