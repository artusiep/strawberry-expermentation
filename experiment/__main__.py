import asyncio

import uvicorn
from experiment.db.base import Base
from experiment.deps import get_engine, get_session_factory
from experiment.management.user.entity import UserEntity
from sqlalchemy import DDL


async def recreate_tables():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.execute(DDL(f"CREATE SCHEMA IF NOT EXISTS {Base.metadata.schema}"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


async def insert_data():
    engine = get_engine()
    async with get_session_factory().begin() as session:
        session.add(
            UserEntity(
                username="test",
                password="$2b$12$tnQJ3U58/OUABfCmruTwnek0JbMXs07LnYxU40M1o5zjD2WXsIrkC",
                roles=["user"],
            )
        )  # password: 'abc'
        session.add(
            UserEntity(
                username="admin-test",
                password="$2b$12$tnQJ3U58/OUABfCmruTwnek0JbMXs07LnYxU40M1o5zjD2WXsIrkC",
                roles=["user", "admin"],
            )
        )  # password: 'abc'

    await engine.dispose()


asyncio.run(recreate_tables())
asyncio.run(insert_data())
uvicorn.run(
    "home_assignment.app:get_app", reload=True, host="localhost", port=8081
)  # noqa: WPS432
