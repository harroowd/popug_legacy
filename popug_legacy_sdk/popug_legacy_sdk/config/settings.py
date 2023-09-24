from pydantic import BaseSettings

from popug_legacy_sdk.config.auth import AuthSettings


class Settings(BaseSettings):
    auth: AuthSettings

    class Config:
        env_file = "config/.env"
        env_nested_delimiter = "__"


settings = Settings()
