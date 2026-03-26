from fastcrud import FastCRUD

from ..models.capture_endpoint_payload import CaptureEndpointPayload
from ..schemas.capture import CaptureEndpointPayloadCreate, CaptureEndpointPayloadRead, CaptureEndpointPayloadUpdate

CRUDCaptureEndpointPayload = FastCRUD[
    CaptureEndpointPayload,
    CaptureEndpointPayloadCreate,
    CaptureEndpointPayloadUpdate,
    CaptureEndpointPayloadUpdate,
    CaptureEndpointPayloadUpdate,
    CaptureEndpointPayloadRead,
]
crud_capture_endpoint_payloads = CRUDCaptureEndpointPayload(CaptureEndpointPayload)
