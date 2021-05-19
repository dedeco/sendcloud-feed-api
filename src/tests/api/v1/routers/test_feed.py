import json
import unittest
from http import HTTPStatus

from _pytest.monkeypatch import MonkeyPatch
from starlette.testclient import TestClient

from app.api.v1.routers import feed
from app.core.config import settings
from app.main import app


class FeedTests(unittest.TestCase):

    def setUp(self):
        self.app = TestClient(app)
        self.monkeypatch = MonkeyPatch()

    def test_add_feed(self):
        test_request_data = {
            "url": "https://feeds.feedburner.com/tweakers/mixed",
            "updates_enabled": True
        }
        test_response_data = {
            "_id": "60a1eaeee74e6c5f9414ef65",
            "url": "https://feeds.feedburner.com/tweakers/mixed",
            "title": "Tweakers",
            "link": "https://tweakers.net/",
            "description": "Tweakers is de grootste hardwaresite en techcommunity van Nederland.",
            "updates_enabled": True
        }

        async def add_feed(payload):
            return 1

        self.monkeypatch.setattr(feed, "add_feed", add_feed)

        response = self.app.post(
            f"{settings.API_V1_STR}/feeds/",
            data=json.dumps(test_request_data),
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == test_response_data

    def test_list_feeds(self):
        response_test_data = [
            {
                "_id": "60a1ea9ae74e6c5f9414ef63",
                "url": "http://www.nu.nl/rss/Algemeen",
                "title": "NU - Algemeen",
                "link": "https://www.nu.nl/algemeen",
                "description": "Het laatste nieuws het eerst op NU.nl",
                "updates_enabled": True
            },
            {
                "_id": "60a1eaeee74e6c5f9414ef65",
                "url": "https://feeds.feedburner.com/tweakers/mixed",
                "title": "Tweakers",
                "link": "https://tweakers.net/",
                "description": "Tweakers is de grootste hardwaresite en techcommunity van Nederland.",
                "updates_enabled": True
            }
        ]

        async def mock_list_feeds():
            return response_test_data

        self.monkeypatch.setattr(feed, "list_feeds", mock_list_feeds)

        response = self.app.get(
            f"{settings.API_V1_STR}/feeds/",
        )
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) > 0
        assert response.json() == response_test_data
