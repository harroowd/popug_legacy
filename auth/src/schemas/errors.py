from typing import Type

from database.models import Base
from fastapi import HTTPException, status
from pydantic import BaseModel


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


def check_raise_data_not_found(data: Type[Base] | None, details: str):
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=details,
        )


def check_raise_data_conflict(data: Type[Base] | None, details: str):
    if data is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=details
        )


def check_raise_unauthorized(data: Type[Base] | None, details: str):
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=details
        )
