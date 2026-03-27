import os
from enum import StrEnum
from typing import Literal

from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _build_redis_url(host: str, port: int, db: int, password: str | None, ssl: bool) -> str:
    scheme = "rediss" if ssl else "redis"
    auth = f":{password}@" if password else ""
    return f"{scheme}://{auth}{host}:{port}/{db}"


class AppSettings(BaseSettings):
    APP_NAME: str = "Black Tonny Backend Base"
    APP_DESCRIPTION: str | None = "Clean FastAPI dual-database base repository."
    APP_VERSION: str = "0.1.0"
    LICENSE_NAME: str | None = "MIT"
    CONTACT_NAME: str | None = None
    CONTACT_EMAIL: str | None = None


class FileLoggerSettings(BaseSettings):
    FILE_LOG_MAX_BYTES: int = 10 * 1024 * 1024
    FILE_LOG_BACKUP_COUNT: int = 5
    FILE_LOG_FORMAT_JSON: bool = True
    FILE_LOG_LEVEL: str = "INFO"

    # Include request ID, path, method, client host, and status code in the file log
    FILE_LOG_INCLUDE_REQUEST_ID: bool = True
    FILE_LOG_INCLUDE_PATH: bool = True
    FILE_LOG_INCLUDE_METHOD: bool = True
    FILE_LOG_INCLUDE_CLIENT_HOST: bool = True
    FILE_LOG_INCLUDE_STATUS_CODE: bool = True


class ConsoleLoggerSettings(BaseSettings):
    CONSOLE_LOG_LEVEL: str = "INFO"
    CONSOLE_LOG_FORMAT_JSON: bool = False

    # Include request ID, path, method, client host, and status code in the console log
    CONSOLE_LOG_INCLUDE_REQUEST_ID: bool = False
    CONSOLE_LOG_INCLUDE_PATH: bool = False
    CONSOLE_LOG_INCLUDE_METHOD: bool = False
    CONSOLE_LOG_INCLUDE_CLIENT_HOST: bool = False
    CONSOLE_LOG_INCLUDE_STATUS_CODE: bool = False


class DatabaseSettings(BaseSettings):
    CAPTURE_DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/capture"
    SERVING_DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/serving"


class CryptSettings(BaseSettings):
    SECRET_KEY: SecretStr = SecretStr("change-this-secret-key-to-32-bytes-min")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


class CookieSettings(BaseSettings):
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"
    COOKIE_PATH: str = "/"
    COOKIE_DOMAIN: str | None = None


class FirstUserSettings(BaseSettings):
    ADMIN_NAME: str = "admin"
    ADMIN_EMAIL: str = "admin@admin.com"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "!Ch4ng3Th1sP4ssW0rd!"


class TierBootstrapSettings(BaseSettings):
    TIER_NAME: str = "free"


class RedisCacheSettings(BaseSettings):
    REDIS_CACHE_ENABLED: bool = False
    REDIS_CACHE_HOST: str = "localhost"
    REDIS_CACHE_PORT: int = 6379
    REDIS_CACHE_DB: int = 0
    REDIS_CACHE_PASSWORD: str | None = None
    REDIS_CACHE_SSL: bool = False

    @computed_field  # type: ignore[prop-decorator]
    @property
    def REDIS_CACHE_URL(self) -> str:
        return _build_redis_url(
            host=self.REDIS_CACHE_HOST,
            port=self.REDIS_CACHE_PORT,
            db=self.REDIS_CACHE_DB,
            password=self.REDIS_CACHE_PASSWORD,
            ssl=self.REDIS_CACHE_SSL,
        )


class ClientSideCacheSettings(BaseSettings):
    CLIENT_CACHE_MAX_AGE: int = 60


class RedisQueueSettings(BaseSettings):
    REDIS_QUEUE_ENABLED: bool = False
    REDIS_QUEUE_HOST: str = "localhost"
    REDIS_QUEUE_PORT: int = 6379
    REDIS_QUEUE_DB: int = 0
    REDIS_QUEUE_PASSWORD: str | None = None
    REDIS_QUEUE_SSL: bool = False

    @computed_field  # type: ignore[prop-decorator]
    @property
    def REDIS_QUEUE_URL(self) -> str:
        return _build_redis_url(
            host=self.REDIS_QUEUE_HOST,
            port=self.REDIS_QUEUE_PORT,
            db=self.REDIS_QUEUE_DB,
            password=self.REDIS_QUEUE_PASSWORD,
            ssl=self.REDIS_QUEUE_SSL,
        )


class RedisRateLimiterSettings(BaseSettings):
    REDIS_RATE_LIMIT_ENABLED: bool = False
    REDIS_RATE_LIMIT_HOST: str = "localhost"
    REDIS_RATE_LIMIT_PORT: int = 6379
    REDIS_RATE_LIMIT_DB: int = 0
    REDIS_RATE_LIMIT_PASSWORD: str | None = None
    REDIS_RATE_LIMIT_SSL: bool = False

    @computed_field  # type: ignore[prop-decorator]
    @property
    def REDIS_RATE_LIMIT_URL(self) -> str:
        return _build_redis_url(
            host=self.REDIS_RATE_LIMIT_HOST,
            port=self.REDIS_RATE_LIMIT_PORT,
            db=self.REDIS_RATE_LIMIT_DB,
            password=self.REDIS_RATE_LIMIT_PASSWORD,
            ssl=self.REDIS_RATE_LIMIT_SSL,
        )


class DefaultRateLimitSettings(BaseSettings):
    DEFAULT_RATE_LIMIT_LIMIT: int = 10
    DEFAULT_RATE_LIMIT_PERIOD: int = 3600


class WorkerScheduleSettings(BaseSettings):
    WORKER_SCHEDULE_ENABLED: bool = False


class EnvironmentOption(StrEnum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = EnvironmentOption.LOCAL


class CORSSettings(BaseSettings):
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]


class Settings(
    AppSettings,
    DatabaseSettings,
    CryptSettings,
    CookieSettings,
    FirstUserSettings,
    TierBootstrapSettings,
    RedisCacheSettings,
    ClientSideCacheSettings,
    RedisQueueSettings,
    RedisRateLimiterSettings,
    DefaultRateLimitSettings,
    WorkerScheduleSettings,
    EnvironmentSettings,
    CORSSettings,
    FileLoggerSettings,
    ConsoleLoggerSettings,
):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
