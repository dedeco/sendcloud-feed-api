from http import HTTPStatus

from fastapi import APIRouter
from starlette.responses import JSONResponse

health_router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@health_router.get("/")
async def health_check():
    return JSONResponse(
            status_code=HTTPStatus.OK,
            content={"ping": "pong!"}
        )
