from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.models.active_log import ActiveLog


class ActiveLogService:
    def create_log(
        self,
        db: Session,
        user_id: int,
        trigger_rule_id: int,
        action_type: str,
        status: str,
        request_payload: dict[str, Any] | None = None,
        response_payload: dict[str, Any] | None = None,
    ) -> ActiveLog:
        log = ActiveLog(
            user_id=user_id,
            trigger_rule_id=trigger_rule_id,
            action_type=action_type,
            status=status,
            request_payload=request_payload,
            response_payload=response_payload,
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    def list_for_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[ActiveLog]:
        stmt = (
            select(ActiveLog)
            .where(ActiveLog.user_id == user_id)
            .order_by(ActiveLog.created_at.desc(), ActiveLog.id.desc())
        )
        return list(db.scalars(stmt).all())

    def get_or_raise(
        self,
        db: Session,
        user_id: int,
        log_id: int,
    ) -> ActiveLog:
        stmt = select(ActiveLog).where(
            ActiveLog.id == log_id,
            ActiveLog.user_id == user_id,
        )
        log = db.scalar(stmt)
        if not log:
            raise BusinessException(
                code=40461,
                message="active log not found",
                status_code=404,
            )
        return log


active_log_service = ActiveLogService()