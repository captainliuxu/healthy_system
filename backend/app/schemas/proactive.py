from datetime import datetime
from pydantic import BaseModel


class ProactiveWindowCreate(BaseModel):
    profile_id: int
    scene: str
    start_time: str
    end_time: str
    enabled: bool = True


class ProactiveWindowRead(BaseModel):
    id: int
    profile_id: int
    scene: str
    start_time: str
    end_time: str
    enabled: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ProactiveTriggerRequest(BaseModel):
    profile_id: int


class ProactiveLogRead(BaseModel):
    id: int
    profile_id: int
    trigger_type: str
    trigger_reason: str
    message_content: str | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}