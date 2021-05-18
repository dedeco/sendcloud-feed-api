from typing import List

from fastapi import APIRouter

MAX_LIST_FEEDS = 1000

from app.core.db import db
from app.models.entry import EntryModel

entry_router = APIRouter(
    prefix="/feeds/entries",
    tags=["entries"],
)


@entry_router.get("/", response_description="List all feeds from a feed", response_model=List[EntryModel])
async def list_entries():
    entries = await  db["entries"].find({'url': 'https://feeds.feedburner.com/tweakers/mixed'}).to_list(MAX_LIST_FEEDS)
    return entries
