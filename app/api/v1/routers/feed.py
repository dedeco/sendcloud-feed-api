from http import HTTPStatus

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.db import db
from app.models.feed import FeedModel
from app.worker.celery_app import celery_app

router = APIRouter(
    prefix="/feeds",
    tags=["feeds"],
)


@router.post("/", response_description="Add a feed", response_model=FeedModel)
async def add_feed(feed: FeedModel = Body(...)):
    feed = jsonable_encoder(feed)
    new_feed = await db["feeds"].insert_one(feed)
    created_feed = await db["feeds"].find_one({"_id": new_feed.inserted_id})
    task = celery_app.send_task("app.worker.celery_worker.test_celery", args=["oiee"])
    print(task)
    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content=created_feed
    )
