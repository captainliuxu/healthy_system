from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.timezone import BeijingDateTime, now_beijing
from app.db.session import Base


class ActiveLog(Base):
    __tablename__ = "active_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    trigger_rule_id: Mapped[int] = mapped_column(
        ForeignKey("trigger_rules.id"),
        nullable=False,
        index=True,
    )
    action_type: Mapped[str] = mapped_column(String(30), nullable=False, default="rule_check")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending", index=True)
    request_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    response_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        BeijingDateTime(),
        default=now_beijing,
        nullable=False,
        index=True,
    )
