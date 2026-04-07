from datetime import datetime
from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    nickname: str | None = None
    age: int | None = None
    gender: str | None = None
    phone: str | None = None
    preferred_call_name: str | None = None
    living_alone: bool = False
    chronic_disease: str | None = None
    medicine_note: str | None = None
    usual_sleep_time: str | None = None
    usual_wake_time: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    allergies: str | None = None
    remark: str | None = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    name: str | None = None
    nickname: str | None = None
    age: int | None = None
    gender: str | None = None
    phone: str | None = None
    preferred_call_name: str | None = None
    living_alone: bool | None = None
    chronic_disease: str | None = None
    medicine_note: str | None = None
    usual_sleep_time: str | None = None
    usual_wake_time: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    allergies: str | None = None
    remark: str | None = None


class ProfileRead(ProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}