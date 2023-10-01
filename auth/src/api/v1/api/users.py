from typing import (
    Any,
    Union,
)

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from popug_legacy_sdk.database.user import ModelRepos
from popug_legacy_sdk.schemas import Pagination

from core.password import Password
from database.database import get_db
from database.models import User
from schemas.errors import (
    EmailExist,
    UsernameExist,
    UserNotFound,
    check_raise,
)
from schemas.users import (
    User as UserSchema,
    UserPayload,
    UsersInfo,
    UsersPayload,
    UserUpdateSchemas,
)
from utils.utils import get_column_name

router_for_admins = APIRouter(prefix="/users", tags=["users"])
router_without_token = APIRouter(prefix="/users", tags=["users"])
router = APIRouter(prefix="/users", tags=["users"])
router_update = APIRouter(prefix="/users", tags=["users"])


@router_without_token.post(
    "/",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "User Conflict",
            "model": Union[
                EmailExist,
                UsernameExist,
            ],
        }
    },
)
async def create_user(payload: UserPayload) -> UserSchema:
    async with get_db() as db:
        user_query = await ModelRepos(db, User).set_filter(
            data=payload.email, field=get_column_name(str(User.email))
        )
        user_data = await user_query.get_one()
        check_raise(
            user_data, status.HTTP_409_CONFLICT, EmailExist().detail, False
        )
        user_query = await ModelRepos(db, User).set_filter(
            data=payload.username, field=get_column_name(str(User.username))
        )
        user_data = await user_query.get_one()
        check_raise(
            user_data, status.HTTP_409_CONFLICT, UsernameExist().detail, False
        )
        payload.password = Password(payload.password).get_password_hash()
        new_user = await ModelRepos(db, User).add(payload.dict())

    return UserSchema(**new_user.__dict__)


@router.get(
    "/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get user by id",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User Conflict",
            "model": UserNotFound,
        }
    },
)
async def get_user(user_id: int) -> UserSchema:
    async with get_db() as db:
        user_query = await ModelRepos(db, User).set_filter(
            data=user_id, field=get_column_name(str(User.id))
        )
        user_data = await user_query.get_one()
    check_raise(user_data, status.HTTP_404_NOT_FOUND, UserNotFound().detail)
    return UserSchema(**user_data.__dict__)


@router_for_admins.get(
    "/",
    response_model=UsersInfo,
    status_code=status.HTTP_200_OK,
    summary="Get all users by filters",
)
async def get_users(payload: UsersPayload = Depends()) -> UsersInfo:
    async with get_db() as db:
        pagination = Pagination(**payload.dict())
        users, count = await ModelRepos(db, User).get_all_data(pagination)
    pagination.count = count
    data = [UserSchema(**user_data.__dict__) for user_data in users]
    return UsersInfo(data=data, pagination=pagination)


@router_update.patch(
    "/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Update username",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found Error",
            "model": UserNotFound,
        },
        status.HTTP_409_CONFLICT: {
            "description": "User conflict",
            "model": UsernameExist,
        },
    },
)
async def update_user(user_id: int, data: UserUpdateSchemas) -> dict[str, Any]:
    async with get_db() as db:
        user_query = await ModelRepos(db, User).set_filter(
            data=data.username, field=get_column_name(str(User.username))
        )
        user_data = await user_query.get_one()
        check_raise(
            user_data, status.HTTP_409_CONFLICT, UsernameExist().detail
        )

        user_query = await ModelRepos(db, User).set_filter(
            data=user_id, field=get_column_name(str(User.id))
        )
        user_data = await user_query.get_one()
        check_raise(
            user_data, status.HTTP_404_NOT_FOUND, UserNotFound().detail
        )

        user_data.username = data.username
        await db.commit()
    return UserSchema(**user_data.__dict__).dict()


@router_for_admins.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user by id",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found Error",
            "model": UserNotFound,
        }
    },
)
async def delete_user(user_id: int):
    async with get_db() as db:
        user_query = await ModelRepos(db, User).set_filter(
            data=user_id, field=get_column_name(str(User.id))
        )
        user_data = await user_query.get_one()
        check_raise(
            user_data, status.HTTP_404_NOT_FOUND, UserNotFound().detail
        )
        await user_query.delete(user_data)
