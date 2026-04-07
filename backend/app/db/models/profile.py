from datetime import UTC, datetime
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(50), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    preferred_call_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    living_alone: Mapped[bool] = mapped_column(Boolean, default=False)
    chronic_disease: Mapped[str | None] = mapped_column(Text, nullable=True)
    medicine_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    usual_sleep_time: Mapped[str | None] = mapped_column(String(20), nullable=True)
    usual_wake_time: Mapped[str | None] = mapped_column(String(20), nullable=True)
    emergency_contact_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    allergies: Mapped[str | None] = mapped_column(Text, nullable=True)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))