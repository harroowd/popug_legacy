from pydantic import BaseModel


class AuthSettings(BaseModel):
    secret_key: str
    algorithm: str
