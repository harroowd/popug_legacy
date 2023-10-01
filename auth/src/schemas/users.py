from datetime import datetime

from fastapi import Query
from popug_legacy_sdk.schemas import (
    Pagination,
    UserRoles,
)
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRoles
    created_at: datetime


class UserPayload(BaseModel):
    email: EmailStr
    password: str
    username: str
    role: UserRoles


class UsersInfo(BaseModel):
    data: list[User]
    pagination: Pagination


class UsersPayload(BaseModel):
    page_size: int = Field(
        Query(default=25, example=25, description="Set a page size.")
    )
    page: int = Field(
        Query(default=1, example=1, description="Set a page number.")
    )


class UserUpdateSchemas(BaseModel):
    username: str
