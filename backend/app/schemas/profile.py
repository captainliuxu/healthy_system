from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProfileBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    age: int | None = Field(default=None, ge=0, le=120)
    gender: str | None = Field(default=None, max_length=20)
    height: float | None = Field(default=None, gt=0, le=250)
    weight: float | None = Field(default=None, gt=0, le=300)
    chronic_history: str | None = None
    allergy_history: str | None = None
    emergency_contact: str | None = Field(default=None, max_length=100)
    remark: str | None = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    age: int | None = Field(default=None, ge=0, le=120)
    gender: str | None = Field(default=None, max_length=20)
    height: float | None = Field(default=None, gt=0, le=250)
    weight: float | None = Field(default=None, gt=0, le=300)
    chronic_history: str | None = None
    allergy_history: str | None = None
    emergency_contact: str | None = Field(default=None, max_length=100)
    remark: str | None = None


class ProfileRead(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)