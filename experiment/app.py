import logging

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from sqlalchemy.ext.asyncio import AsyncEngine

from .deps import get_engine
from .router import router

logger = logging.getLogger(__name__)


def get_local_app(engine: AsyncEngine) -> FastAPI:
    local_app = FastAPI(
        title="assignment",
        default_response_class=UJSONResponse,
    )

    @local_app.on_event("shutdown")
    async def dispose_db_engine() -> None:
        logger.debug("Disposing the database engine")
        await engine.dispose()

    local_app.include_router(router=router)

    return local_app


def get_app() -> FastAPI:
    engine = get_engine()
    return get_local_app(engine)
