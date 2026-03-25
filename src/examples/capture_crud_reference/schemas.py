from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ExampleRecordCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    external_key: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=128)


class ExampleRecordRead(BaseModel):
    id: int
    external_key: str
    name: str
    created_at: datetime


class ExampleRecordUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=128)
