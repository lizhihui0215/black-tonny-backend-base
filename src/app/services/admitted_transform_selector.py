from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.crud_capture_batches import get_capture_batch_read
from ..crud.crud_capture_endpoint_payloads import list_capture_endpoint_payload_reads
from ..schemas.capture import CaptureBatchStatus
from ..schemas.transform import (
    AdmittedTransformBatchSnapshot,
    AdmittedTransformInputSnapshot,
    AdmittedTransformPayloadSnapshot,
)


def _build_batch_snapshot(
    *,
    capture_batch_id: str,
    batch_status: CaptureBatchStatus,
    transformed_at: datetime | None,
    error_message: str | None,
) -> AdmittedTransformBatchSnapshot:
    return AdmittedTransformBatchSnapshot(
        capture_batch_id=capture_batch_id,
        batch_status=batch_status,
        transformed_at=transformed_at,
        error_message=error_message,
    )


def _build_payload_snapshot(
    *,
    capture_batch_id: str,
    source_endpoint: str,
    payload_json: str,
    checksum: str,
    pulled_at: datetime,
) -> AdmittedTransformPayloadSnapshot:
    return AdmittedTransformPayloadSnapshot(
        capture_batch_id=capture_batch_id,
        source_endpoint=source_endpoint,
        payload_json=payload_json,
        checksum=checksum,
        pulled_at=pulled_at,
    )


async def select_admitted_transform_input(
    db: AsyncSession,
    *,
    capture_batch_id: str,
) -> AdmittedTransformInputSnapshot | None:
    batch = await get_capture_batch_read(
        db=db,
        capture_batch_id=capture_batch_id,
    )
    if batch is None:
        return None

    payload_response = await list_capture_endpoint_payload_reads(
        db=db,
        capture_batch_id=capture_batch_id,
        limit=None,
    )
    payloads = payload_response["data"]
    if not payloads:
        return None

    return AdmittedTransformInputSnapshot(
        batch=_build_batch_snapshot(
            capture_batch_id=batch.capture_batch_id,
            batch_status=batch.batch_status,
            transformed_at=batch.transformed_at,
            error_message=batch.error_message,
        ),
        payloads=[
            _build_payload_snapshot(
                capture_batch_id=payload.capture_batch_id,
                source_endpoint=payload.source_endpoint,
                payload_json=payload.payload_json,
                checksum=payload.checksum,
                pulled_at=payload.pulled_at,
            )
            for payload in payloads
        ],
    )
