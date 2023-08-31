from functools import cache
from pathlib import Path

from pydantic_settings import BaseSettings

env_file = Path(__file__).parent / ".env"


class Settings(BaseSettings):
    DEBUG: bool = False
    JSON_LOGS: bool = False
    REALNAME: str = "vicky"
    USERNAME: str = "vicky"
    SERVER: str = "localhost"
    PORT: int = 6667
    CHANNELS: list[str] = ["#main"]

    class Config:
        env_file = env_file.absolute() if env_file.exists() else None


@cache
def get_settings():
    return Settings()


settings = get_settings()
