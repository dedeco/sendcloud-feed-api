import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FeedAPI"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    MONGO_DB: str = "feed"
    MONGO_URL: str = "mongodb:27017"
    MONGO_URI: str = f"mongodb://{MONGO_URL}/{MONGO_DB}"

    class Config:
        env_file = ".env"


settings = Settings()
