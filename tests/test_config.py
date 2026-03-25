from src.app.core.config import settings


def test_redis_urls_include_db_password_and_ssl() -> None:
    original_values = (
        settings.REDIS_CACHE_HOST,
        settings.REDIS_CACHE_PORT,
        settings.REDIS_CACHE_DB,
        settings.REDIS_CACHE_PASSWORD,
        settings.REDIS_CACHE_SSL,
        settings.REDIS_QUEUE_HOST,
        settings.REDIS_QUEUE_PORT,
        settings.REDIS_QUEUE_DB,
        settings.REDIS_QUEUE_PASSWORD,
        settings.REDIS_QUEUE_SSL,
        settings.REDIS_RATE_LIMIT_HOST,
        settings.REDIS_RATE_LIMIT_PORT,
        settings.REDIS_RATE_LIMIT_DB,
        settings.REDIS_RATE_LIMIT_PASSWORD,
        settings.REDIS_RATE_LIMIT_SSL,
    )

    settings.REDIS_CACHE_HOST = "cache.example.com"
    settings.REDIS_CACHE_PORT = 6380
    settings.REDIS_CACHE_DB = 2
    settings.REDIS_CACHE_PASSWORD = "cache-secret"
    settings.REDIS_CACHE_SSL = True

    settings.REDIS_QUEUE_HOST = "queue.example.com"
    settings.REDIS_QUEUE_PORT = 6381
    settings.REDIS_QUEUE_DB = 3
    settings.REDIS_QUEUE_PASSWORD = "queue-secret"
    settings.REDIS_QUEUE_SSL = False

    settings.REDIS_RATE_LIMIT_HOST = "rate.example.com"
    settings.REDIS_RATE_LIMIT_PORT = 6382
    settings.REDIS_RATE_LIMIT_DB = 4
    settings.REDIS_RATE_LIMIT_PASSWORD = "rate-secret"
    settings.REDIS_RATE_LIMIT_SSL = True

    try:
        assert settings.REDIS_CACHE_URL == "rediss://:cache-secret@cache.example.com:6380/2"
        assert settings.REDIS_QUEUE_URL == "redis://:queue-secret@queue.example.com:6381/3"
        assert settings.REDIS_RATE_LIMIT_URL == "rediss://:rate-secret@rate.example.com:6382/4"
    finally:
        (
            settings.REDIS_CACHE_HOST,
            settings.REDIS_CACHE_PORT,
            settings.REDIS_CACHE_DB,
            settings.REDIS_CACHE_PASSWORD,
            settings.REDIS_CACHE_SSL,
            settings.REDIS_QUEUE_HOST,
            settings.REDIS_QUEUE_PORT,
            settings.REDIS_QUEUE_DB,
            settings.REDIS_QUEUE_PASSWORD,
            settings.REDIS_QUEUE_SSL,
            settings.REDIS_RATE_LIMIT_HOST,
            settings.REDIS_RATE_LIMIT_PORT,
            settings.REDIS_RATE_LIMIT_DB,
            settings.REDIS_RATE_LIMIT_PASSWORD,
            settings.REDIS_RATE_LIMIT_SSL,
        ) = original_values
