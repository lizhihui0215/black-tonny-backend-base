import asyncio
import logging
from typing import Any

import structlog
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def sample_background_task(ctx: dict[str, Any], payload: str) -> str:
    _ = ctx
    await asyncio.sleep(0)
    return f"Task {payload} is complete!"


async def sample_scheduled_task(ctx: dict[str, Any]) -> dict[str, str]:
    _ = ctx
    logging.info("Scheduled reference task executed")
    return {"status": "scheduled"}


async def startup(ctx: dict[str, Any]) -> None:
    _ = ctx
    logging.info("Worker Started")


async def shutdown(ctx: dict[str, Any]) -> None:
    _ = ctx
    logging.info("Worker end")


async def on_job_start(ctx: dict[str, Any]) -> None:
    structlog.contextvars.bind_contextvars(job_id=ctx["job_id"])
    logging.info("Job Started")


async def on_job_end(ctx: dict[str, Any]) -> None:
    logging.info("Job Completed")
    structlog.contextvars.clear_contextvars()
