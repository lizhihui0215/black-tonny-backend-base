from datetime import datetime

from pydantic import BaseModel


class ExampleReadModel(BaseModel):
    id: int
    external_key: str
    display_name: str
    last_synced_at: datetime | None = None
