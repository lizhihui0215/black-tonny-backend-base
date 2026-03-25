from collections.abc import Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.serving_database import async_get_serving_db

from .schemas import ExampleReadModel

router = APIRouter(prefix="/example-read-models", tags=["example-reference"])


@router.get("", response_model=list[ExampleReadModel])
async def list_example_read_models(
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(async_get_serving_db),
) -> list[ExampleReadModel]:
    query = text(
        """
        SELECT id, external_key, display_name, last_synced_at
        FROM example_read_model
        ORDER BY id
        LIMIT :limit
        """
    )
    result = await db.execute(query, {"limit": limit})
    rows: Sequence[RowMapping] = result.mappings().all()
    return [ExampleReadModel.model_validate(row) for row in rows]
