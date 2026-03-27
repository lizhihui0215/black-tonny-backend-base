from src.app.constants.capture import (
    CAPTURE_BATCH_DEFAULT_STATUS,
    CAPTURE_BATCH_ID_MAX_LENGTH,
    CAPTURE_CHECKSUM_MAX_LENGTH,
    CAPTURE_PAGE_CURSOR_MAX_LENGTH,
    CAPTURE_ROUTE_KIND_MAX_LENGTH,
    CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH,
    CAPTURE_SOURCE_NAME_MAX_LENGTH,
)
from src.app.models.capture_batch import CaptureBatch
from src.app.models.capture_endpoint_payload import CaptureEndpointPayload
from src.app.schemas.capture import (
    CaptureBatchCreate,
    CaptureBatchUpdate,
    CaptureEndpointPayloadCreate,
    CaptureEndpointPayloadUpdate,
)


def test_capture_constants_match_batch_defaults_and_schema_lengths() -> None:
    batch_create_schema = CaptureBatchCreate.model_json_schema()["properties"]
    batch_update_schema = CaptureBatchUpdate.model_json_schema()["properties"]

    assert CaptureBatch.__table__.c.batch_status.default.arg == CAPTURE_BATCH_DEFAULT_STATUS
    assert CaptureBatchCreate.model_fields["batch_status"].default == CAPTURE_BATCH_DEFAULT_STATUS

    assert CaptureBatch.__table__.c.capture_batch_id.type.length == CAPTURE_BATCH_ID_MAX_LENGTH
    assert batch_create_schema["capture_batch_id"]["maxLength"] == CAPTURE_BATCH_ID_MAX_LENGTH

    assert CaptureBatch.__table__.c.source_name.type.length == CAPTURE_SOURCE_NAME_MAX_LENGTH
    assert batch_create_schema["source_name"]["maxLength"] == CAPTURE_SOURCE_NAME_MAX_LENGTH
    assert batch_update_schema["source_name"]["anyOf"][0]["maxLength"] == CAPTURE_SOURCE_NAME_MAX_LENGTH


def test_capture_constants_match_payload_model_and_schema_lengths() -> None:
    payload_create_schema = CaptureEndpointPayloadCreate.model_json_schema()["properties"]
    payload_update_schema = CaptureEndpointPayloadUpdate.model_json_schema()["properties"]

    assert payload_create_schema["capture_batch_id"]["maxLength"] == CAPTURE_BATCH_ID_MAX_LENGTH

    assert CaptureEndpointPayload.__table__.c.source_endpoint.type.length == CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH
    assert payload_create_schema["source_endpoint"]["maxLength"] == CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH
    assert payload_update_schema["source_endpoint"]["anyOf"][0]["maxLength"] == CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH

    assert CaptureEndpointPayload.__table__.c.route_kind.type.length == CAPTURE_ROUTE_KIND_MAX_LENGTH
    assert payload_create_schema["route_kind"]["anyOf"][0]["maxLength"] == CAPTURE_ROUTE_KIND_MAX_LENGTH
    assert payload_update_schema["route_kind"]["anyOf"][0]["maxLength"] == CAPTURE_ROUTE_KIND_MAX_LENGTH

    assert CaptureEndpointPayload.__table__.c.page_cursor.type.length == CAPTURE_PAGE_CURSOR_MAX_LENGTH
    assert payload_create_schema["page_cursor"]["anyOf"][0]["maxLength"] == CAPTURE_PAGE_CURSOR_MAX_LENGTH
    assert payload_update_schema["page_cursor"]["anyOf"][0]["maxLength"] == CAPTURE_PAGE_CURSOR_MAX_LENGTH

    assert CaptureEndpointPayload.__table__.c.checksum.type.length == CAPTURE_CHECKSUM_MAX_LENGTH
    assert payload_create_schema["checksum"]["maxLength"] == CAPTURE_CHECKSUM_MAX_LENGTH
    assert payload_update_schema["checksum"]["anyOf"][0]["maxLength"] == CAPTURE_CHECKSUM_MAX_LENGTH
