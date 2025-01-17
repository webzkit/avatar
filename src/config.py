from enum import Enum
from os import getenv
from typing import List, Union
from pydantic import Field, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

""" Project setting """


class EnviromentOption(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class AppSetting(BaseSettings):
    APP_NAME: str = Field(default="AppName")
    APP_API_PREFIX: str = Field(default="/api/v1")
    APP_ENV: Union[EnviromentOption, str] = Field(default="development")
    APP_PORT: int = Field(default=8000)

    BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], str] = getenv(
        "BACKEND_CORS_ORIGINS", []
    )

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


class PostgresSetting(BaseSettings):
    POSTGRES_USER: str = getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = int(getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = getenv("AVATAR_APP_DB", "avatars")
    POSTGRES_SYNC_PREFIX: str = getenv("POSTGRES_SYNC_PREFIX", "postgresql://")
    POSTGRES_ASYNC_PREFIX: str = getenv(
        "POSTGRES_ASYNC_PREFIX", "postgresql+asyncpg://"
    )
    POSTGRES_URI: str = (
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


class RedisCacheSetting(BaseSettings):
    REDIS_CACHE_HOST: str = getenv("REDIS_HOST", "redis")
    REDIS_CACHE_PASSWORD: str = getenv("REDIS_PASSWORD", "secret")
    REDIS_CACHE_PORT: int = int(getenv("REDIS_PORT", 6379))

    REDIS_CACHE_URL: str = (
        f"redis://:{REDIS_CACHE_PASSWORD}@{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}"
    )


class ServiceSetting(BaseSettings):
    ENGINE_SERVICE_URL: str = getenv("ENGINE_SERVICE_URL", "")
    OWNER_ENGINE_SERVICE_URL: str = getenv("/api/v1/users/", "")
    HTTP_TIMEOUT_SERVICE: int = int(getenv("HTTP_TIMEOUT_SERVICE", 59))


class Settings(AppSetting, PostgresSetting, RedisCacheSetting, ServiceSetting):
    model_config = SettingsConfigDict(env_prefix="AVATAR_")
    pass


settings = Settings()
