from fastapi import FastAPI

from app.api.v1.routers.entry import entry_router
from app.api.v1.routers.feed import feed_router
from app.api.v1.routers.health import health_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(feed_router, prefix=settings.API_V1_STR)
app.include_router(entry_router, prefix=settings.API_V1_STR)
