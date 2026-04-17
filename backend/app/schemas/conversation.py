from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ConversationStatus(str, Enum):
    active = "active"
    archived = "archived"


class ConversationCreate(BaseModel):
    title: str | None = Field(default=None, max_length=100)


class ConversationTitleUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)


class ConversationRead(BaseModel):
    id: int
    user_id: int
    title: str
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationListData(BaseModel):
    items: list[ConversationRead]