from fastcrud import FastCRUD

from .model import ExampleRecord
from .schemas import ExampleRecordCreate, ExampleRecordRead, ExampleRecordUpdate

CRUDExampleRecord = FastCRUD[
    ExampleRecord,
    ExampleRecordCreate,
    ExampleRecordUpdate,
    ExampleRecordUpdate,
    ExampleRecordUpdate,
    ExampleRecordRead,
]

example_record_crud = CRUDExampleRecord(ExampleRecord)
