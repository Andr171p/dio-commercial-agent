import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

from .constants import ENV_PATH


load_dotenv(ENV_PATH)


class EmbeddingsSettings(BaseSettings):
    MODEL_NAME: str = os.getenv("EMBEDDINGS_MODEL_NAME")  # 1024 dimensional
    MODEL_KWARGS: dict = {"device": "cpu"}
    ENCODE_KWARGS: dict = {"normalize_embeddings": False}


class PineconeSettings(BaseSettings):
    API_KEY: str = os.getenv("PINECONE_API_KEY")


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


class PostgresSettings(BaseSettings):
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    @property
    def url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class GigaChatSettings(BaseSettings):
    API_KEY: str = os.getenv("GIGACHAT_API_KEY")
    SCOPE: str = os.getenv("GIGACHAT_SCOPE")
    MODEL_NAME: str = os.getenv("GIGACHAT_MODEL_NAME")


class YandexGPTSettings(BaseSettings):
    FOLDER_ID: str = os.getenv("YANDEX_FOLDER_ID")
    API_KEY: str = os.getenv("YANDEX_GPT_API_KEY")


class Settings(BaseSettings):
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    pinecone: PineconeSettings = PineconeSettings()
    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()
    giga_chat: GigaChatSettings = GigaChatSettings()
    yandex_gpt: YandexGPTSettings = YandexGPTSettings()
