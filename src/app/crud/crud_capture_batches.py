from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.capture_batch import CaptureBatch
from ..schemas.capture import (
    CaptureBatchCreate,
    CaptureBatchRead,
    CaptureBatchReadListResponse,
    CaptureBatchStatus,
    CaptureBatchUpdate,
)

CRUDCaptureBatch = FastCRUD[
    CaptureBatch,
    CaptureBatchCreate,
    CaptureBatchUpdate,
    CaptureBatchUpdate,
    CaptureBatchUpdate,
    CaptureBatchRead,
]
crud_capture_batches = CRUDCaptureBatch(CaptureBatch)


async def get_capture_batch_read(
    db: AsyncSession,
    *,
    capture_batch_id: str,
) -> CaptureBatchRead | None:
    return await crud_capture_batches.get(
        db=db,
        capture_batch_id=capture_batch_id,
        schema_to_select=CaptureBatchRead,
        return_as_model=True,
    )


async def list_capture_batch_reads(
    db: AsyncSession,
    *,
    offset: int = 0,
    limit: int | None = 100,
    batch_status: CaptureBatchStatus | None = None,
    source_name: str | None = None,
) -> CaptureBatchReadListResponse:
    filters: dict[str, object] = {}
    if batch_status is not None:
        filters["batch_status"] = batch_status
    if source_name is not None:
        filters["source_name"] = source_name

    return await crud_capture_batches.get_multi(
        db=db,
        offset=offset,
        limit=limit,
        schema_to_select=CaptureBatchRead,
        sort_columns="capture_batch_id",
        sort_orders="asc",
        return_as_model=True,
        return_total_count=True,
        **filters,
    )
