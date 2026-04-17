from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TriggerRuleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    trigger_type: str = Field(..., min_length=1, max_length=50)
    enabled: bool = True
    condition_json: dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=100, ge=0, le=9999)


class TriggerRuleCreate(TriggerRuleBase):
    pass


class TriggerRuleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    trigger_type: str | None = Field(default=None, min_length=1, max_length=50)
    enabled: bool | None = None
    condition_json: dict[str, Any] | None = None
    priority: int | None = Field(default=None, ge=0, le=9999)


class TriggerRuleRead(TriggerRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TriggerRuleListData(BaseModel):
    items: list[TriggerRuleRead]


class TriggerRuleCheckData(BaseModel):
    log_id: int
    rule_id: int
    user_id: int
    action_type: str
    status: str
    triggered: bool
    reason: str
    response_payload: dict[str, Any] | None = None
    created_at: datetime