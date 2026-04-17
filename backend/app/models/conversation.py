from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.timezone import BeijingDateTime, now_beijing
from app.db.session import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False, default="New Conversation")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active", index=True)
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
