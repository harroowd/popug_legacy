from pydantic import BaseModel, EmailStr


class TokenPayload(BaseModel):
    email: EmailStr
    password: str


class TokenSchemas(BaseModel):
    access_token: str
    refresh_token: str


class TokenRefreshSchemas(BaseModel):
    access_token: str


class TokenRefreshPayload(BaseModel):
    refresh_token: str
