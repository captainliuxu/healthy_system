from datetime import datetime
from pydantic import BaseModel, Field


class RecordCreate(BaseModel):
    profile_id: int
    record_type: str = Field(..., min_length=1, max_length=30)
    source: str | None = None
    value_json: str
    note: str | None = None
    recorded_at: datetime | None = None


class RecordRead(BaseModel):
    id: int
    profile_id: int
    record_type: str
    source: str | None = None
    value_json: str
    note: str | None = None
    recorded_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}