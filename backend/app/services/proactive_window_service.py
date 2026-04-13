from __future__ import annotations

from datetime import datetime, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.models.proactive_window import ProactiveWindow
from app.schemas.proactive import ProactiveWindowUpdate


class ProactiveWindowService:
    def get_or_create_for_user(
        self,
        db: Session,
        user_id: int,
    ) -> ProactiveWindow:
        window = self._get_by_user_id(db, user_id)
        if window:
            return window

        window = ProactiveWindow(
            user_id=user_id,
            enabled=True,
            quiet_hours_start="22:00",
            quiet_hours_end="08:00",
            max_trigger_per_day=1,
        )
        db.add(window)
        db.commit()
        db.refresh(window)
        return window

    def update_for_user(
        self,
        db: Session,
        user_id: int,
        payload: ProactiveWindowUpdate,
    ) -> ProactiveWindow:
        self._validate_time_range(
            payload.quiet_hours_start,
            payload.quiet_hours_end,
        )

        window = self.get_or_create_for_user(db, user_id)
        window.enabled = payload.enabled
        window.quiet_hours_start = payload.quiet_hours_start
        window.quiet_hours_end = payload.quiet_hours_end
        window.max_trigger_per_day = payload.max_trigger_per_day

        db.add(window)
        db.commit()
        db.refresh(window)
        return window

    def allow_trigger_now(
        self,
        window: ProactiveWindow,
        now: datetime | None = None,
    ) -> tuple[bool, str]:
        if not window.enabled:
            return False, "proactive window is disabled"

        current_time = (now or datetime.now()).time().replace(
            second=0,
            microsecond=0,
        )
        quiet_start = self._parse_time_text(window.quiet_hours_start)
        quiet_end = self._parse_time_text(window.quiet_hours_end)

        if self._is_in_quiet_hours(current_time, quiet_start, quiet_end):
            return False, "current time is inside quiet hours"

        return True, "allowed"

    def _get_by_user_id(
        self,
        db: Session,
        user_id: int,
    ) -> ProactiveWindow | None:
        stmt = select(ProactiveWindow).where(ProactiveWindow.user_id == user_id)
        return db.scalar(stmt)

    def _validate_time_range(
        self,
        start_text: str,
        end_text: str,
    ) -> None:
        self._parse_time_text(start_text)
        self._parse_time_text(end_text)

        if start_text == end_text:
            raise BusinessException(
                code=40071,
                message="quiet_hours_start cannot be equal to quiet_hours_end",
                status_code=400,
            )

    def _parse_time_text(self, value: str) -> time:
        try:
            return datetime.strptime(value, "%H:%M").time()
        except ValueError as exc:
            raise BusinessException(
                code=40072,
                message="time format must be HH:MM",
                status_code=400,
            ) from exc

    def _is_in_quiet_hours(
        self,
        current_time: time,
        quiet_start: time,
        quiet_end: time,
    ) -> bool:
        if quiet_start < quiet_end:
            return quiet_start <= current_time < quiet_end

        return current_time >= quiet_start or current_time < quiet_end


proactive_window_service = ProactiveWindowService()