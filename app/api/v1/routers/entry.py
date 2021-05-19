from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.models.base import PyObjectId
from app.models.entry_update import UpdateEntryModel

MAX_LIST_FEEDS = 1000

from app.core.db import db
from app.models.entry import EntryModel

entry_router = APIRouter(
    prefix="/feeds/entries",
    tags=["entries"],
)


@entry_router.get("/", response_description="List all feeds from a feed", response_model=List[EntryModel])
async def list_entries(url: Optional[str] = None, read: Optional[bool] = None):
    query = {}
    if url:
        query.update({'url': url})
    if read is not None:
        query.update({'read': read})
    entries = await db["entries"].find(query).to_list(MAX_LIST_FEEDS)
    return entries


@entry_router.put("/{id}", response_description="Mark as read")
async def mark_as_read(id: str):
    if entry := await db["entries"].find_one({"_id": PyObjectId(id)}):
        update_result = await db["entries"].update_one({"_id": PyObjectId(id)}, {'$set': {'read': True}})
        if update_result.modified_count == 1:
            return JSONResponse(
                status_code=HTTPStatus.NO_CONTENT,
            )
        else:
            return JSONResponse(
                status_code=HTTPStatus.ALREADY_REPORTED,
                content={"message": f"Entry {id} was marked as read before"}
            )
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=f"Entry {id} not found"
    )
