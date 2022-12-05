import typing

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker
from strawberry.fastapi import BaseContext
from strawberry.types import Info

from ..deps import get_session_factory


class Context(BaseContext):
    def __init__(self, session_factory: sessionmaker):
        super().__init__()

        self.session_factory = session_factory
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SiepInfo = Info[Context, typing.Any]


async def get_context(
    session_factory: sessionmaker = Depends(get_session_factory),
) -> Context:  # noqa: B008, WPS404
    return Context(session_factory)
