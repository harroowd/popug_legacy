from config.auth import AuthSettings
from config.database import DatabaseSettings
from config.redis import RedisSettings
from pydantic import BaseSettings


class Settings(BaseSettings):
    database: DatabaseSettings
    auth: AuthSettings
    redis: RedisSettings

    class Config:
        env_file = "config/.env"
        env_nested_delimiter = "__"


settings = Settings()
