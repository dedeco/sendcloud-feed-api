from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, HttpUrl


class UpdateEntryModel(BaseModel):
    url: str
    title: str
    link: HttpUrl
    author: Optional[str]
    summary: Optional[str]
    read: Optional[bool]
    last_updated: datetime
    last_read: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "url": "https://www.nu.nl/tech/6133462/onbemande-chinese-verkenner-geland-op-mars.html",
                "title": "Onbemande Chinese verkenner geland op Mars",
                "link": "https://www.nu.nl/algemeen",
                "author": "ANP/NU.nl",
                "summary": "Een onbemande Chinese verkenner is zaterdagochtend succesvol geland op de planeet Mars. "
                           "Dat melden Chinese staatsmedia, verwijzend naar de China National Space Administration. "
                           "De landing van Zhurong, zoals de verkenner heet, is een triomf voor Peking, dat steeds "
                           "meer ambities heeft op het gebied van ruimtevaart.",
                "read": False,
                "updated": "2021-05-18T21:52:43.388525"
            }
        }
