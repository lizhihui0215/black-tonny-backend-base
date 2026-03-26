from fastcrud import FastCRUD

from ..models.capture_batch import CaptureBatch
from ..schemas.capture import CaptureBatchCreate, CaptureBatchRead, CaptureBatchUpdate

CRUDCaptureBatch = FastCRUD[
    CaptureBatch,
    CaptureBatchCreate,
    CaptureBatchUpdate,
    CaptureBatchUpdate,
    CaptureBatchUpdate,
    CaptureBatchRead,
]
crud_capture_batches = CRUDCaptureBatch(CaptureBatch)
