from abc import ABC
from typing import Any, Union

from experiment.auth_helper import get_user_from_header
from experiment.management.user.type import UserRole
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry import BasePermission
from strawberry.types import Info


class RolePermission(ABC, BasePermission):
    message = "User is not authenticated or not allowed for given operation."
    role = None

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Union[Request, WebSocket] = info.context.request
        if "Authorization" in request.headers:
            if user := await get_user_from_header(
                info, request.headers["Authorization"]
            ):
                if self.role in user.roles:
                    info.context.request.state.user = user
                    return True
        return False


class UserPermission(RolePermission):
    role = UserRole.user.value


class AdminPermission(RolePermission):
    role = UserRole.admin.value
