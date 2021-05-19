import unittest
from http import HTTPStatus

from starlette.testclient import TestClient

from app.core.config import settings
from app.main import app


class HealthTests(unittest.TestCase):

    def setUp(self):
        self.app = TestClient(app)

    def test_ping(self):
        response = self.app.get(
            f"{settings.API_V1_STR}/health"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"ping": "pong!"}
