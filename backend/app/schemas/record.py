from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class RecordType(str, Enum):
    checkin = "checkin"
    blood_pressure = "blood_pressure"
    blood_glucose = "blood_glucose"
    sleep = "sleep"
    medication = "medication"
    mood = "mood"


class RecordBase(BaseModel):
    record_type: RecordType
    value: str = Field(..., min_length=1, max_length=100)
    unit: str | None = Field(default=None, max_length=30)
    note: str | None = Field(default=None, max_length=500)


class RecordCreate(RecordBase):
    record_time: datetime | None = None


class RecordUpdate(BaseModel):
    record_type: RecordType | None = None
    value: str | None = Field(default=None, min_length=1, max_length=100)
    unit: str | None = Field(default=None, max_length=30)
    note: str | None = Field(default=None, max_length=500)
    record_time: datetime | None = None

# 给前端的读取结构
class RecordRead(RecordBase):
    id: int
    user_id: int
    record_time: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecordQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=50)
    record_type: RecordType | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

#定义分页列表最终返回的数据结构。
class RecordListData(BaseModel):
    items: list[RecordRead]
    total: int
    page: int
    page_size: int
    total_pages: int