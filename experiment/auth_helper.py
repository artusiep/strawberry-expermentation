from datetime import timedelta
from typing import Optional

import arrow
from experiment.deps import get_settings
from experiment.management.user.database import query_user
from experiment.management.user.entity import UserEntity
from jose import ExpiredSignatureError, JWTError, jwt
from strawberry.types import Info


class AuthenticationFailed(Exception):
    def __init__(self, message):
        self.message = message


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = arrow.utcnow() + expires_delta
    else:
        expire = arrow.utcnow().shift(minutes=15)
    to_encode.update({"exp": expire.datetime})
    encoded_jwt = jwt.encode(
        to_encode,
        get_settings().secret_key,
        algorithm=get_settings().jwt_token_algorithm,
    )
    return encoded_jwt


def get_access_token(authorization_header: str):
    auth = authorization_header.split()

    if auth[0].lower() != "bearer":
        return None

    if len(auth) == 1:
        msg = 'Invalid "bearer" header: No credentials provided.'
        raise AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = 'Invalid "bearer" header: Credentials string should not contain spaces.'
        raise AuthenticationFailed(msg)

    return auth[1]


async def get_user_from_access_token(info: Info, access_token) -> Optional[UserEntity]:
    try:
        payload = jwt.decode(
            access_token,
            get_settings().secret_key,
            algorithms=get_settings().jwt_token_algorithm,
        )

        if not (username := payload.get("sub")):
            msg = "Access token does not contain user info."
            raise AuthenticationFailed(msg)
    except ExpiredSignatureError as e:
        msg = "Access token signature has expired."
        raise AuthenticationFailed(msg) from e
    except JWTError as e:
        msg = "Error during decoding access token."
        raise AuthenticationFailed(msg) from e
    async with info.context.session_factory.begin() as session:
        user = await query_user(session, username)
        return user
    return None


async def get_user_from_header(
    info: Info, authorization_header: str
) -> Optional[UserEntity]:
    access_token = get_access_token(authorization_header)
    return await get_user_from_access_token(info, access_token)
