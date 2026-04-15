from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.models.proactive_message import ProactiveMessage
from app.models.trigger_rule import TriggerRule


class ProactiveMessageService:
    def create_message(
        self,
        db: Session,
        user_id: int,
        trigger_rule: TriggerRule,
        title: str,
        content: str,
    ) -> ProactiveMessage:
        message = ProactiveMessage(
            user_id=user_id,
            trigger_rule_id=trigger_rule.id,
            trigger_type=trigger_rule.trigger_type,
            title=title,
            content=content,
            status="pending",
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def list_for_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[ProactiveMessage]:
        stmt = (
            select(ProactiveMessage)
            .where(ProactiveMessage.user_id == user_id)
            .order_by(
                ProactiveMessage.created_at.desc(),
                ProactiveMessage.id.desc(),
            )
        )
        return list(db.scalars(stmt).all())

    def list_pending_for_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[ProactiveMessage]:
        stmt = (
            select(ProactiveMessage)
            .where(
                ProactiveMessage.user_id == user_id,
                ProactiveMessage.status == "pending",
            )
            .order_by(
                ProactiveMessage.created_at.asc(),
                ProactiveMessage.id.asc(),
            )
        )
        return list(db.scalars(stmt).all())

    def get_or_raise(
        self,
        db: Session,
        user_id: int,
        message_id: int,
    ) -> ProactiveMessage:
        stmt = select(ProactiveMessage).where(
            ProactiveMessage.id == message_id,
            ProactiveMessage.user_id == user_id,
        )
        message = db.scalar(stmt)
        if not message:
            raise BusinessException(
                code=40471,
                message="proactive message not found",
                status_code=404,
            )
        return message

    def mark_displayed(
        self,
        db: Session,
        user_id: int,
        message_id: int,
    ) -> ProactiveMessage:
        message = self.get_or_raise(db, user_id, message_id)

        if message.status != "displayed":
            message.status = "displayed"
            message.displayed_at = datetime.now(UTC)
            db.add(message)
            db.commit()
            db.refresh(message)

        return message


proactive_message_service = ProactiveMessageService()
