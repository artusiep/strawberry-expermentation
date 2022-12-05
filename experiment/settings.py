import logging
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, StrictStr
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine as aio_create_async_engine

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    secret_key: StrictStr = Field(StrictStr, min_length=50, env="SECRET_KEY")
    jwt_token_algorithm = "HS256"
    access_token_expire_minutes: int = Field(
        default=15,
        description="This implementation does not support token revocation so expiration time need to small",
    )

    host: str = Field(default="localhost", env="PGHOST")
    port: int = Field(default=5432, env="PGPORT")  # noqa: WPS432
    username: str = Field(default="postgres", env="PGUSER")
    password: Optional[str] = Field(env="PGPASSWORD")
    database: str = Field("postgres", env="PGDATABASE")
    drivername: str = Field("postgresql+asyncpg")

    @property
    def url(self) -> URL:
        params: Dict[str, Any] = {
            "drivername": self.drivername,
            "host": self.host,
            "database": self.database,
            "username": self.username,
        }

        if self.password is not None:
            params["password"] = self.password

        port_opt = self.port
        if port_opt is not None:
            params["port"] = port_opt

        return URL.create(**params)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "."


def create_async_engine(settings: Settings) -> AsyncEngine:
    logger.debug(
        "Creating a database engine with the connection string %s",
        settings.url.render_as_string(hide_password=True),
    )

    return aio_create_async_engine(settings.url)
