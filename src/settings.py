"""Server configuration."""

import os

from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv

_ = load_dotenv()


@dataclass()
class Settings:
    """Get settingd from environment variables."""

    MONGO_URI: str = os.environ["MONGO_URI"]
    MONGO_PASSWORD: str = os.environ["MONGO_PASSWORD"]
    MONGO_DATABASE: str = os.environ["MONGO_DATABASE"]


@lru_cache
def get_settings() -> Settings:
    """Cache settings instance.

    Returns:
        Settings: The settings instance.
    """
    return Settings()


CONFIG = get_settings()
