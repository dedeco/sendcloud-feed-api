from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, HttpUrl

from app.models.base import PyObjectId


class EntryModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    url: Optional[str] = Field(...)
    title: Optional[str] = Field(...)
    link: Optional[HttpUrl] = Field(...)
    author: Optional[str] = Field(...)
    summary: Optional[str] = Field(...)
    read: Optional[bool] = Field(...)
    last_updated: datetime = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "url": "https://feeds.feedburner.com/tweakers/mixed",
                "title": "No Man's Sky en twee andere VR-games krijgen Nvidia DLSS-ondersteuning",
                "link": "https://tweakers.net/nieuws/181808/no-mans-sky-en-twee-andere-vr-games-krijgen-nvidia-dlss"
                        "-ondersteuning.html",
                "author": "Julian Huijbregts",
                "summary": "Nvidia kondigt aan dat er DLSS-ondersteuning aan negen games is toegevoegd. Voor het eerst "
                           "zitten daar ook VR-games bij: No Man's Sky, Into The Radius en Wrench. De rendertechniek die "
                           "framerates flink kan verhogen, kan goed van pas komen bij VR-games.<img "
                           "src=\"http://feeds.feedburner.com/~r/tweakers/mixed/~4/3NBndTzeh6U\" height=\"1\" width=\"1\" "
                           "alt=\"\"/>",
                "read": False
            }
        }
