from fastapi import FastAPI

from app.api.v1.routers.feed import router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router, prefix=settings.API_V1_STR)

