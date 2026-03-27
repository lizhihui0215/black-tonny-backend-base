import json
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.crud_capture_batches import crud_capture_batches, get_capture_batch_read
from ..crud.crud_capture_endpoint_payloads import crud_capture_endpoint_payloads, get_capture_endpoint_payload_read
from ..schemas.capture import (
    CaptureBatchCreate,
    CaptureBatchRead,
    CaptureBatchStatus,
    CaptureBatchUpdate,
    CaptureEndpointPayloadCreate,
    CaptureEndpointPayloadRead,
)


def _serialize_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _build_checksum(payload_json: str) -> str:
    return sha256(payload_json.encode("utf-8")).hexdigest()


def _new_capture_batch_id() -> str:
    return uuid4().hex


async def create_capture_batch(
    db: AsyncSession,
    *,
    source_name: str,
    capture_batch_id: str | None = None,
    batch_status: CaptureBatchStatus = "queued",
    pulled_at: datetime | None = None,
    transformed_at: datetime | None = None,
    error_message: str | None = None,
) -> CaptureBatchRead:
    resolved_capture_batch_id = capture_batch_id or _new_capture_batch_id()

    await crud_capture_batches.create(
        db=db,
        object=CaptureBatchCreate(
            capture_batch_id=resolved_capture_batch_id,
            batch_status=batch_status,
            source_name=source_name,
            pulled_at=pulled_at,
            transformed_at=transformed_at,
            error_message=error_message,
        ),
        schema_to_select=CaptureBatchRead,
    )

    created_batch = await get_capture_batch_read(
        db=db,
        capture_batch_id=resolved_capture_batch_id,
    )
    if created_batch is None:
        raise RuntimeError("capture batch was not readable after create")

    return created_batch


async def update_capture_batch(
    db: AsyncSession,
    *,
    capture_batch_id: str,
    values: CaptureBatchUpdate,
) -> CaptureBatchRead | None:
    existing_batch = await get_capture_batch_read(
        db=db,
        capture_batch_id=capture_batch_id,
    )
    if existing_batch is None:
        return None

    await crud_capture_batches.update(
        db=db,
        object=values,
        capture_batch_id=capture_batch_id,
    )

    return await get_capture_batch_read(
        db=db,
        capture_batch_id=capture_batch_id,
    )


async def append_capture_payload(
    db: AsyncSession,
    *,
    capture_batch_id: str,
    source_endpoint: str,
    payload: Any,
    request_params: Any | None = None,
    route_kind: str | None = None,
    page_cursor: str | None = None,
    page_no: int | None = None,
    pulled_at: datetime | None = None,
) -> CaptureEndpointPayloadRead:
    payload_json = _serialize_json(payload)
    request_params_json = None if request_params is None else _serialize_json(request_params)
    resolved_pulled_at = pulled_at or datetime.now(UTC)

    created_payload = await crud_capture_endpoint_payloads.create(
        db=db,
        object=CaptureEndpointPayloadCreate(
            capture_batch_id=capture_batch_id,
            source_endpoint=source_endpoint,
            route_kind=route_kind,
            page_cursor=page_cursor,
            page_no=page_no,
            request_params=request_params_json,
            payload_json=payload_json,
            checksum=_build_checksum(payload_json),
            pulled_at=resolved_pulled_at,
        ),
        schema_to_select=CaptureEndpointPayloadRead,
    )

    payload_id = created_payload.id if hasattr(created_payload, "id") else created_payload["id"]
    persisted_payload = await get_capture_endpoint_payload_read(
        db=db,
        id=payload_id,
    )
    if persisted_payload is None:
        raise RuntimeError("capture endpoint payload was not readable after create")

    return persisted_payload
