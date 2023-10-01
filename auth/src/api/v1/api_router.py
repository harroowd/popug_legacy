from fastapi import (
    APIRouter,
    Security,
)
from popug_legacy_sdk.auth.permissions import (
    check_permissions,
    check_update_user_permissions,
)
from popug_legacy_sdk.schemas import UserRoles

from api.v1.api import (
    auth,
    users,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(
    users.router_for_admins,
    dependencies=[
        Security(check_permissions, scopes=[str(UserRoles.ADMIN.value)])
    ],
)
api_router.include_router(users.router_without_token)
api_router.include_router(
    users.router_update,
    dependencies=[
        Security(
            check_update_user_permissions,
            scopes=[
                str(user.value)
                for user in UserRoles
                if user != UserRoles.ADMIN
            ],
        )
    ],
)
api_router.include_router(
    users.router,
    dependencies=[
        Security(
            check_permissions, scopes=[str(user.value) for user in UserRoles]
        )
    ],
)
