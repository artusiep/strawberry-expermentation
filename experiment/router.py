from fastapi import Response
from fastapi.routing import APIRouter
from experiment import graphql
from starlette.status import HTTP_200_OK

router = APIRouter()
router.include_router(graphql.router, prefix="/graphql")


@router.get("/")
async def default() -> Response:
    return Response(status_code=HTTP_200_OK)
