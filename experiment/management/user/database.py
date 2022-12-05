import datetime

import arrow
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...scalars import SiepPasswordType
from .entity import UserEntity
from .type import UserRole


async def query_users(session: AsyncSession) -> list[UserEntity]:
    results = await session.execute(select(UserEntity))
    return results.scalars().fetchall()


async def query_user(session: AsyncSession, username: str) -> UserEntity:
    results = await session.execute(
        select(UserEntity).filter(UserEntity.username == username)
    )
    return results.scalar_one()


async def create_user(
    session: AsyncSession,
    username: str,
    hashed_password: SiepPasswordType,
    roles: list[UserRole],
) -> UserEntity:
    user = UserEntity(username=username, password=hashed_password, roles=[role.value for role in roles])
    session.add(user)
    await session.commit()
    return user


async def change_user_password(
    session: AsyncSession,
    username: str,
    new_hashed_password: SiepPasswordType,
    password_modified_at: arrow.Arrow,
) -> UserEntity:
    user = await query_user(session, username)
    user.password = new_hashed_password
    user.password_modified_at = password_modified_at
    await session.commit()
    return user
