from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .settings import Settings, create_async_engine

_settings = Settings()


def get_settings() -> Settings:
    return _settings


_engine = create_async_engine(_settings)


def get_engine() -> AsyncEngine:
    return _engine


_session_factory = sessionmaker(
    bind=_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)


def get_session_factory() -> sessionmaker:
    return _session_factory
