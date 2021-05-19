from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.db import db
from app.models.feed import FeedModel
from app.models.feed_update import UpdateFeedModel
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


@feed_router.put("/{id}", response_description="Update a feed and/force an update (entries)", response_model=FeedModel)
async def update_feed(id: str, feed: UpdateFeedModel = Body(...)):
    feed = {k: v for k, v in feed.dict().items() if v is not None}

    if len(feed) >= 1:
        update_result = await db["feeds"].update_one({"_id": id}, {"$set": feed})
        if update_result.modified_count == 1:
            celery_app.send_task("app.workers.entries.tasks.update_feed", args=[id])
            print('enviei')
            if (updated_feed := await db["feeds"].find_one({"_id": id})) is not None:
                if updated_feed.get('last_updated'):
                    celery_app.send_task("app.workers.entries.tasks.update_feed_item", args=[updated_feed.get("url")])
                return updated_feed

    if (existing_feed := await db["feeds"].find_one({"_id": id})) is not None:
        return existing_feed

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=f"Feed {id} not found"
    )
