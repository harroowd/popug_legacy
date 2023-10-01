from datetime import datetime

from fastapi import (
    APIRouter,
    status,
)
from popug_legacy_sdk.auth.token import decode_token
from popug_legacy_sdk.database.user import ModelRepos
from popug_legacy_sdk.schemas import TokenData

from config.settings import settings
from core.password import Password
from database.database import get_db
from database.models import User
from schemas.errors import (
    WrongCreds,
    WrongToken,
    check_raise,
)
from schemas.token import (
    TokenPayload,
    TokenRefreshPayload,
    TokenRefreshSchemas,
    TokenSchemas,
)
from utils.utils import get_column_name

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
        user = await ModelRepos(db, User).get_by_field(
            data=payload.email, field=get_column_name(str(User.email))
        )
        if user and Password(payload.password).verify_password(user.password):
            user.current_sign_in_at = datetime.utcnow()
            await db.commit()
    check_raise(
        user, status.HTTP_401_UNAUTHORIZED, details=WrongCreds().detail
    )

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
