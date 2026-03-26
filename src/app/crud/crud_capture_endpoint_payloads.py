from typing import cast

from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.capture_endpoint_payload import CaptureEndpointPayload
from ..schemas.capture import (
    CaptureEndpointPayloadCreate,
    CaptureEndpointPayloadRead,
    CaptureEndpointPayloadReadListResponse,
    CaptureEndpointPayloadUpdate,
)

CRUDCaptureEndpointPayload = FastCRUD[
    CaptureEndpointPayload,
    CaptureEndpointPayloadCreate,
    CaptureEndpointPayloadUpdate,
    CaptureEndpointPayloadUpdate,
    CaptureEndpointPayloadUpdate,
    CaptureEndpointPayloadRead,
]
crud_capture_endpoint_payloads = CRUDCaptureEndpointPayload(CaptureEndpointPayload)


async def get_capture_endpoint_payload_read(
    db: AsyncSession,
    *,
    id: int,
) -> CaptureEndpointPayloadRead | None:
    return await crud_capture_endpoint_payloads.get(
        db=db,
        id=id,
        schema_to_select=CaptureEndpointPayloadRead,
        return_as_model=True,
    )


async def list_capture_endpoint_payload_reads(
    db: AsyncSession,
    *,
    capture_batch_id: str | None = None,
    source_endpoint: str | None = None,
    offset: int = 0,
    limit: int | None = 100,
) -> CaptureEndpointPayloadReadListResponse:
    filters: dict[str, object] = {}
    if capture_batch_id is not None:
        filters["capture_batch_id"] = capture_batch_id
    if source_endpoint is not None:
        filters["source_endpoint"] = source_endpoint

    response = await crud_capture_endpoint_payloads.get_multi(
        db=db,
        offset=offset,
        limit=limit,
        schema_to_select=CaptureEndpointPayloadRead,
        sort_columns="id",
        sort_orders="asc",
        return_as_model=True,
        return_total_count=True,
        **filters,
    )

    return cast(
        CaptureEndpointPayloadReadListResponse,
        {
            "data": response["data"],
            "total_count": response["total_count"],
        },
    )
