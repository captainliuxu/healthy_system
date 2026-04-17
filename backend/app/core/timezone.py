from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator

BEIJING_TIMEZONE = ZoneInfo("Asia/Shanghai")


def ensure_beijing_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=BEIJING_TIMEZONE)
    return value.astimezone(BEIJING_TIMEZONE)


def now_beijing() -> datetime:
    return datetime.now(BEIJING_TIMEZONE)


class BeijingDateTime(TypeDecorator[datetime]):
    impl = DateTime
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(DateTime(timezone=False))

    def process_bind_param(
        self,
        value: datetime | None,
        dialect,
    ) -> datetime | None:
        if value is None:
            return None

        beijing_value = ensure_beijing_datetime(value)
        return beijing_value.replace(tzinfo=None)

    def process_result_value(
        self,
        value: datetime | None,
        dialect,
    ) -> datetime | None:
        if value is None:
            return None
        return ensure_beijing_datetime(value)
