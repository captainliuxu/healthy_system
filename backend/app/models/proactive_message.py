from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.timezone import BeijingDateTime, now_beijing
from app.db.session import Base


class ProactiveMessage(Base):
    __tablename__ = "proactive_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    trigger_rule_id: Mapped[int | None] = mapped_column(
        ForeignKey("trigger_rules.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    trigger_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        BeijingDateTime(),
        default=now_beijing,
        nullable=False,
        index=True,
    )
    displayed_at: Mapped[datetime | None] = mapped_column(
        BeijingDateTime(),
        nullable=True,
    )
