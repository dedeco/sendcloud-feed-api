from http import HTTPStatus
from unittest import TestCase

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)
SOME_FEED = {
    "url": "http://www.nu.nl/rss/Algemeen",
    "title": "NU - Algemeen",
    "link": "https://www.nu.nl/algemeen",
    "author": "Freddie Mercury",
    "updates_enabled": True,
}


class EverythingEquals:
    def __eq__(self, other):
        return True


everything_equals = EverythingEquals()


class TestFeed(TestCase):

    def test_add_feed(self):
        response = client.post(
            f"{settings.API_V1_STR}/feeds/",
            json=SOME_FEED,
        )
        created_feed = response.json()
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(created_feed,  {
            "url": "http://www.nu.nl/rss/Algemeen",
            "title": "NU - Algemeen",
            "link": "https://www.nu.nl/algemeen",
            "author": "Freddie Mercury",
            "updates_enabled": True,
            "_id": everything_equals
        })
