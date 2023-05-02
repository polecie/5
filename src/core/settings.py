from functools import lru_cache
from pydantic import BaseSettings, Field, ValidationError

from src.core.resources import ApiResources

# base_dir = Path(__file__).resolve().parent.parent.parent

__all__ = ("settings",)


class ApiSettings(BaseSettings):
    resources = ApiResources

    host: str = Field("localhost", env="API_HOST")
    port: int = Field(8000, env="API_PORT")
    description: str = Field(
        "Api",
        env="API_DESCRIPTION"
    )
    version: str = Field("0.1.0", env="API_VERSION")
    title: str = Field("Api.bot", env="API_TITLE")
    debug: bool = Field(True, env="API_DEBUG")

    class Config:
        env_file_encoding = 'utf-8'
        env_file = ".env", ".env.dev", ".env.prod"


class PostgresSettings(BaseSettings):
    host: str = Field("localhost", env="DB_HOST")
    port: int = Field(5432, env="DB_PORT")
    user: str = Field("polecie", env="DB_USER")
    password: str = Field("polecie", env="DB_PASSWORD")
    db_name: str = Field("demo", env="DB_NAME")
    echo: bool = Field(True, env="DB_ECHO")
    # url: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
    url: str = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"

    class Config:
        env_file_encoding = 'utf-8'
        env_file = ".env", ".env.dev", ".env.prod"


class Settings(BaseSettings):
    api: ApiSettings
    db: PostgresSettings


@lru_cache()
def get_settings() -> Settings:
    try:
        return Settings(
            api=ApiSettings(),
            db=PostgresSettings()
        )
    except ValidationError:
        print("No .env was found")


settings = get_settings()
settings.db.url = settings.db.url.format(
    user=settings.db.user,
    password=settings.db.password,
    host=settings.db.host,
    port=settings.db.port,
    db_name=settings.db.db_name
)
