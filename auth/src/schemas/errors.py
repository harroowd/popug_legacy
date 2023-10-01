from typing import Type

from fastapi import (
    HTTPException,
    status,
)
from pydantic import BaseModel

from database.models import Base


class NoContextError(Exception):
    pass


class UsernameExist(BaseModel):
    detail: str = "User with this username already exists"


class UserNotFound(BaseModel):
    detail: str = "User not found"


class EmailExist(BaseModel):
    detail: str = "User with this email already exists"


class WrongCreds(BaseModel):
    detail: str = "Wrong credentials"


class WrongToken(BaseModel):
    detail: str = "Invalid token."


def check_raise(
    data: Type[Base] | None,
    http_status: status,
    details: str,
    check_empty: bool = True,
):
    if (data is None and check_empty) or (not check_empty and data):
        raise HTTPException(status_code=http_status, detail=details)
