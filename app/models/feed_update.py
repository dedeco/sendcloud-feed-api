from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, AnyUrl, HttpUrl


class UpdateFeedModel(BaseModel):
    url: AnyUrl
    title: Optional[str]
    link: Optional[HttpUrl]
    description: Optional[str]
    updates_enabled: Optional[bool]

    class Config:
        arbitrary_types_allowed = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "url": "http://www.nu.nl/rss/Algemeen",
                "title": "NU - Algemeen",
                "link": "https://www.nu.nl/algemeen",
                "description": "Lorem ipsum",
                "updates_enabled": True,
            }
        }
