import pydantic
from bson import ObjectId
from pydantic import Field, BaseModel, HttpUrl, AnyUrl

from app.models.base import PyObjectId


class FeedModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    url: AnyUrl = Field(...)
    title: str = Field(...)
    link: HttpUrl = Field(...)
    author: str = Field(...)
    updates_enabled: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "url": "http://www.nu.nl/rss/Algemeen",
                "title": "NU - Algemeen",
                "link": "https://www.nu.nl/algemeen",
                "author": "Freddie Mercury",
                "updates_enabled": True,
            }
        }
