from config.settings import settings
from core.security import Security
from database.database import get_db
from database.models import User
from fastapi import APIRouter, status
from schemas.errors import WrongCreds, WrongToken, check_raise_unauthorized
from schemas.token import (
    TokenPayload,
    TokenRefreshPayload,
    TokenRefreshSchemas,
    TokenSchemas,
)
from utils.utils import get_column_name

from popug_legacy_sdk.auth.token import decode_token
from popug_legacy_sdk.database.user import ModelRepos
from popug_legacy_sdk.schemas import TokenData

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token",
    response_model=TokenSchemas,
    status_code=status.HTTP_201_CREATED,
    summary="get access token",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Wrong Creds Error",
            "model": WrongCreds,
        },
    },
)
async def get_token(
    payload: TokenPayload,
) -> TokenSchemas:
    async with get_db() as db:
        user_data = await ModelRepos(db, User).get_by_field(
            data=payload.email, field=get_column_name(str(User.email))
        )
        print(user_data, "KEKEK", user_data.password)
        user = await Security(payload.password).verify_account(user_data, db)
        check_raise_unauthorized(user, details=WrongCreds().detail)

    access_token_data = TokenData(**user.__dict__).generate_token(
        settings.auth.expired_token
    )
    refresh_token_data = TokenData(**user.__dict__).generate_token(
        settings.auth.expired_refresh_token
    )

    return TokenSchemas(
        access_token=access_token_data, refresh_token=refresh_token_data
    )


@router.post(
    "/refresh_token",
    response_model=TokenRefreshSchemas,
    status_code=status.HTTP_201_CREATED,
    summary="refresh access token",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Token Error",
            "model": WrongToken,
        },
    },
)
def refresh_token(payload: TokenRefreshPayload) -> TokenRefreshSchemas:
    payload = decode_token(payload.refresh_token)

    return TokenRefreshSchemas(
        access_token=TokenData(**payload.dict()).generate_token(
            settings.auth.expired_token
        )
    )
