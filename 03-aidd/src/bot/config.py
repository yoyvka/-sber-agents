from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Telegram
    TELEGRAM_TOKEN: str = "YOUR_TOKEN"

    # LLM provider + model
    LLM_PROVIDER: str = "openrouter"  # openrouter | openai
    LLM_MODEL: str = "gpt-4o-mini"
    OPENROUTER_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    LLM_TIMEOUT: int = 15

    # Dialog/history
    HISTORY_MAX_MESSAGES: int = 10

    # Logging
    LOG_LEVEL: str = "INFO"  # DEBUG | INFO | WARNING | ERROR

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # reads from env/.env





