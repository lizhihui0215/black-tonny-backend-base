from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.capture_database import async_get_capture_db

from .crud import example_record_crud
from .schemas import ExampleRecordCreate, ExampleRecordRead, ExampleRecordUpdate

router = APIRouter(prefix="/example-records", tags=["example-reference"])


@router.post("", response_model=ExampleRecordRead, status_code=status.HTTP_201_CREATED)
async def create_example_record(
    payload: ExampleRecordCreate,
    db: AsyncSession = Depends(async_get_capture_db),
) -> dict[str, Any]:
    return await example_record_crud.create(db=db, object=payload, schema_to_select=ExampleRecordRead)


@router.get("/{record_id}", response_model=ExampleRecordRead)
async def read_example_record(
    record_id: int,
    db: AsyncSession = Depends(async_get_capture_db),
) -> dict[str, Any] | None:
    return await example_record_crud.get(db=db, id=record_id, schema_to_select=ExampleRecordRead)


@router.patch("/{record_id}")
async def update_example_record(
    record_id: int,
    payload: ExampleRecordUpdate,
    db: AsyncSession = Depends(async_get_capture_db),
) -> dict[str, str]:
    await example_record_crud.update(db=db, object=payload, id=record_id)
    return {"message": "Example record updated"}
