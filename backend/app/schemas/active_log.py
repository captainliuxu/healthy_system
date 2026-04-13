from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ActiveLogRead(BaseModel):
    id: int
    user_id: int
    trigger_rule_id: int
    action_type: str
    status: str
    request_payload: dict[str, Any] | None = None
    response_payload: dict[str, Any] | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ActiveLogListData(BaseModel):
    items: list[ActiveLogRead]