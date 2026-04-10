from datetime import datetime
from pydantic import BaseModel


class ConversationCreate(BaseModel):
    profile_id: int
    title: str | None = None


class ConversationRead(BaseModel):
    id: int
    profile_id: int
    title: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MessageRead(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    message_type: str
    created_at: datetime

    model_config = {"from_attributes": True}