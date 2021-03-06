from typing import Optional

from bson import ObjectId
from pydantic import Field, BaseModel, HttpUrl, AnyUrl

from app.models.base import PyObjectId


class FeedModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    url: AnyUrl = Field(...)
    title: Optional[str]
    link:  Optional[HttpUrl]
    description: Optional[str]
    updates_enabled: Optional[bool]
    retries: Optional[int] = 0

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "url": "http://www.nu.nl/rss/Algemeen",
                "updates_enabled": True,
            }
        }
