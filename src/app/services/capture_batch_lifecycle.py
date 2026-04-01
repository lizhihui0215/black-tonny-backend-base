from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.crud_capture_batches import get_capture_batch_read
from ..schemas.capture import CaptureBatchRead, CaptureBatchUpdate
from .capture_write import update_capture_batch

_CAPTURED_STATUS = "captured"


def _validate_captured_source_state(batch_status: str) -> None:
    if batch_status != _CAPTURED_STATUS:
        raise ValueError("capture batch must be in the captured state before lifecycle helper writes")


async def mark_capture_batch_transformed(
    db: AsyncSession,
    *,
    capture_batch_id: str,
    transformed_at: datetime | None = None,
) -> CaptureBatchRead | None:
    existing_batch = await get_capture_batch_read(
        db=db,
        capture_batch_id=capture_batch_id,
    )
    if existing_batch is None:
        return None

    _validate_captured_source_state(existing_batch.batch_status)

    return await update_capture_batch(
        db=db,
        capture_batch_id=capture_batch_id,
        values=CaptureBatchUpdate(
            batch_status="transformed",
            transformed_at=transformed_at or datetime.now(UTC),
        ),
    )


async def mark_capture_batch_failed(
    db: AsyncSession,
    *,
    capture_batch_id: str,
    error_message: str,
) -> CaptureBatchRead | None:
    existing_batch = await get_capture_batch_read(
        db=db,
        capture_batch_id=capture_batch_id,
    )
    if existing_batch is None:
        return None

    _validate_captured_source_state(existing_batch.batch_status)

    return await update_capture_batch(
        db=db,
        capture_batch_id=capture_batch_id,
        values=CaptureBatchUpdate(
            batch_status="failed",
            error_message=error_message,
        ),
    )
