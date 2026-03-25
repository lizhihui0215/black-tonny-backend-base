import asyncio
from typing import cast

from arq.cli import watch_reload
from arq.connections import RedisSettings
from arq.cron import cron
from arq.typing import WorkerSettingsType
from arq.worker import check_health, run_worker

from ...core.config import settings
from ...core.logger import logging  # noqa: F401
from .functions import on_job_end, on_job_start, sample_background_task, sample_scheduled_task, shutdown, startup


class WorkerSettings:
    functions = [sample_background_task]
    redis_settings = RedisSettings(
        host=settings.REDIS_QUEUE_HOST,
        port=settings.REDIS_QUEUE_PORT,
        database=settings.REDIS_QUEUE_DB,
        password=settings.REDIS_QUEUE_PASSWORD,
        ssl=settings.REDIS_QUEUE_SSL,
    )
    cron_jobs = (
        [cron(sample_scheduled_task, minute={0}, unique=True, job_id="cron:sample_scheduled_task")]
        if settings.WORKER_SCHEDULE_ENABLED
        else []
    )
    on_startup = startup
    on_shutdown = shutdown
    on_job_start = on_job_start
    on_job_end = on_job_end
    handle_signals = False


def start_arq_service(check: bool = False, burst: int | None = None, watch: str | None = None) -> None:
    if not settings.REDIS_QUEUE_ENABLED:
        raise RuntimeError("REDIS_QUEUE_ENABLED is false. Enable it before starting the worker service.")

    worker_settings_ = cast("WorkerSettingsType", WorkerSettings)
    if check:
        exit(check_health(worker_settings_))

    kwargs = {} if burst is None else {"burst": burst}
    if watch:
        asyncio.run(watch_reload(watch, worker_settings_))
    else:
        run_worker(worker_settings_, **kwargs)


if __name__ == "__main__":
    start_arq_service()
