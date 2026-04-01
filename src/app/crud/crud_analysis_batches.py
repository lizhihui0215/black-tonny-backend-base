from typing import cast

from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.analysis_batch import AnalysisBatch
from ..schemas.analysis import (
    AnalysisBatchCreate,
    AnalysisBatchRead,
    AnalysisBatchReadListResponse,
    AnalysisBatchUpdate,
)

CRUDAnalysisBatch = FastCRUD[
    AnalysisBatch,
    AnalysisBatchCreate,
    AnalysisBatchUpdate,
    AnalysisBatchUpdate,
    AnalysisBatchUpdate,
    AnalysisBatchRead,
]
crud_analysis_batches = CRUDAnalysisBatch(AnalysisBatch)


async def get_analysis_batch_read(
    db: AsyncSession,
    *,
    analysis_batch_id: str,
) -> AnalysisBatchRead | None:
    return await crud_analysis_batches.get(
        db=db,
        analysis_batch_id=analysis_batch_id,
        schema_to_select=AnalysisBatchRead,
        return_as_model=True,
    )


async def list_analysis_batch_reads(
    db: AsyncSession,
    *,
    offset: int = 0,
    limit: int | None = 100,
    batch_status: str | None = None,
    capture_batch_id: str | None = None,
) -> AnalysisBatchReadListResponse:
    filters: dict[str, object] = {}
    if batch_status is not None:
        filters["batch_status"] = batch_status
    if capture_batch_id is not None:
        filters["capture_batch_id"] = capture_batch_id

    response = await crud_analysis_batches.get_multi(
        db=db,
        offset=offset,
        limit=limit,
        schema_to_select=AnalysisBatchRead,
        sort_columns="analysis_batch_id",
        sort_orders="asc",
        return_as_model=True,
        return_total_count=True,
        **filters,
    )

    return cast(
        AnalysisBatchReadListResponse,
        {
            "data": response["data"],
            "total_count": response["total_count"],
        },
    )
