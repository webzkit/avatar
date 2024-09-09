from os import getenv
from typing import Optional, Any, List, Union
from pydantic import Field, PostgresDsn, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

''' Project setting '''


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AVATAR_")

    APP_NAME: str = ""
    APP_API_PREFIX: str = ""
    APP_DOMAIN: str = getenv("AVATAR_APP_DOMAIN", "http://zkit.local")
    APP_ENV: str = getenv("AVATAR_APP_ENV", "development")
    APP_PORT: str = getenv("AVATAR_APP_PORT", "80")

    BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], str] = getenv(
        "BACKEND_CORS_ORIGINS", [])

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def db_connection(cls, v: Optional[str]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            username=getenv("POSTGRES_USER"),
            password=getenv("POSTGRES_PASSWORD"),
            host=getenv("POSTGRES_HOST", ""),
            port=int(getenv("POSTGRES_PORT", "5432")),
            path=f"{getenv('AVATAR_APP_DB') or '/'}",
        )


settings = Settings()
