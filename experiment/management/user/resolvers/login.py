from datetime import timedelta

import strawberry
from experiment.auth_helper import create_access_token
from experiment.deps import get_settings
from experiment.graphql.context import SiepInfo
from experiment.management.user.database import query_user
from experiment.management.user.type import User
from experiment.scalars import SiepPasswordType


@strawberry.input
class LoginInput:
    username: str
    password: SiepPasswordType


@strawberry.type
class LoginSuccess:
    user: User
    access_token: str


@strawberry.type
class LoginError:
    message: str


LoginResult = strawberry.union("LoginResult", (LoginSuccess, LoginError))


async def login(info: SiepInfo, login_input: LoginInput) -> LoginResult:
    async with info.context.session_factory.begin() as session:
        user = await query_user(session, login_input.username)

    if user is None:
        return LoginError(message="User with given username not found")
    if not login_input.password.verify_password(info, user.password):
        return LoginError(message="Given password is invalid ")
    access_token_expires = timedelta(minutes=get_settings().access_token_expire_minutes)
    access_token = create_access_token(
        {"sub": user.username, "role": user.role}, access_token_expires
    )
    return LoginSuccess(user=User.marshal(user), access_token=access_token)
