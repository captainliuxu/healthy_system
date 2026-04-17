from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.timezone import BeijingDateTime, now_beijing
from app.db.session import Base


class ProactiveWindow(Base):
    __tablename__ = "proactive_windows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    quiet_hours_start: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
        default="22:00",
    )
    quiet_hours_end: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
        default="08:00",
    )
    max_trigger_per_day: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    created_at: Mapped[datetime] = mapped_column(
        BeijingDateTime(),
        default=now_beijing,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        BeijingDateTime(),
        default=now_beijing,
        onupdate=now_beijing,
        nullable=False,
    )
