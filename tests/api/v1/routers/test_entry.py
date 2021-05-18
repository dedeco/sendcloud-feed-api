import unittest
from http import HTTPStatus

from _pytest.monkeypatch import MonkeyPatch
from starlette.testclient import TestClient

from app.api.v1.routers import entry
from app.core.config import settings
from app.main import app


class EverythingEquals:
    def __eq__(self, other):
        return True


everything_equals = EverythingEquals()


class EntryTests(unittest.TestCase):

    def setUp(self):
        self.app = TestClient(app)
        self.monkeypatch = MonkeyPatch()

    def test_list_entries(self):
        response_test_data = [
            {
                "_id": "60a3d9b5deebdcba47644c08",
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
            },
            {
                "_id": "60a3d9b5deebdcba47644c09",
                "url": "https://feeds.feedburner.com/tweakers/mixed",
                "title": "Actie-rpg The Ascent met cyberpunkthema verschijnt op 29 juli voor Xbox en pc",
                "link": "https://tweakers.net/nieuws/181806/actie-rpg-the-ascent-met-cyberpunkthema-verschijnt-op-29-juli"
                        "-voor-xbox-en-pc.html",
                "author": "Julian Huijbregts",
                "summary": "The Ascent, een game die door de makers wordt omschreven als een actieshooter-rpg, verschijnt op 29 "
                           "juli voor Xbox-consoles en op Steam. De Xbox-versie is ook onderdeel van Game Pass. Het spel heeft "
                           "een cyberpunkthema en kan coop of solo gespeeld worden.<img "
                           "src=\"http://feeds.feedburner.com/~r/tweakers/mixed/~4/1q_ynoBcJtQ\" height=\"1\" width=\"1\" "
                           "alt=\"\"/>",
                "read": False
            }, ]

        async def mock_list_entries():
            return response_test_data

        self.monkeypatch.setattr(entry, "list_entries", mock_list_entries)

        response = self.app.get(
            f"{settings.API_V1_STR}/feeds/entries/"
        )
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) > 0
        # assert response.json() == response_test_data
