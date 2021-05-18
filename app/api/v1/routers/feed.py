from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.db import db
from app.models.feed import FeedModel
from app.workers.worker import celery_app

MAX_LIST_FEEDS = 1000

feed_router = APIRouter(
    prefix="/feeds",
    tags=["feeds"],
)


@feed_router.post("/", response_description="Add a feed", response_model=FeedModel)
async def add_feed(feed: FeedModel = Body(...)):
    feed = jsonable_encoder(feed)
    existing_feed = await db["feeds"].find_one({"url": feed.get('url')})
    if existing_feed:
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=existing_feed
        )
    new_feed = await db["feeds"].insert_one(feed)
    celery_app.send_task("app.workers.entries.tasks.update_feed", args=[new_feed.inserted_id])
    created_feed = await db["feeds"].find_one({"_id": new_feed.inserted_id})
    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content=created_feed
    )


@feed_router.get("/", response_description="List all feeds", response_model=List[FeedModel])
async def list_feeds():
    feeds = await db["feeds"].find().to_list(MAX_LIST_FEEDS)
    return feeds



