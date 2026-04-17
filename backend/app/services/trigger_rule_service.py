# 要同时负责三件事:
#
# 规则的增删改查
# 规则评估
# 手动检查时写主动日志

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.record import Record
from app.models.trigger_rule import TriggerRule
from app.schemas.trigger_rule import TriggerRuleCreate, TriggerRuleUpdate
from app.services.active_log_service import active_log_service


class TriggerRuleService:
    @staticmethod
    def _as_utc_datetime(value: datetime) -> datetime:
        # SQLite often returns naive datetimes even when the app writes UTC values.
        # Normalize them before any Python-side comparison.
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    def create(
        self,
        db: Session,
        payload: TriggerRuleCreate,
    ) -> TriggerRule:
        rule = TriggerRule(
            name=payload.name.strip(),
            trigger_type=payload.trigger_type.strip(),
            enabled=payload.enabled,
            condition_json=payload.condition_json,
            priority=payload.priority,
        )
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule

    def list_all(self, db: Session) -> list[TriggerRule]:
        stmt = select(TriggerRule).order_by(
            TriggerRule.priority.asc(),
            TriggerRule.id.asc(),
        )
        return list(db.scalars(stmt).all())

    def get_or_raise(self, db: Session, rule_id: int) -> TriggerRule:
        rule = db.get(TriggerRule, rule_id)
        if not rule:
            raise BusinessException(
                code=40462,
                message="trigger rule not found",
                status_code=404,
            )
        return rule

    def update(
        self,
        db: Session,
        rule_id: int,
        payload: TriggerRuleUpdate,
    ) -> TriggerRule:
        rule = self.get_or_raise(db, rule_id)
        update_data = payload.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] is not None:
            update_data["name"] = update_data["name"].strip()

        if (
            "trigger_type" in update_data
            and update_data["trigger_type"] is not None
        ):
            update_data["trigger_type"] = update_data["trigger_type"].strip()

        for field, value in update_data.items():
            setattr(rule, field, value)

        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule

    def delete(self, db: Session, rule_id: int) -> None:
        rule = self.get_or_raise(db, rule_id)
        db.delete(rule)
        db.commit()

    def evaluate_for_user(
        self,
        db: Session,
        user_id: int,
        rule: TriggerRule,
    ) -> dict[str, Any]:
        if not rule.enabled:
            return {
                "triggered": False,
                "reason": "rule is disabled",
                "trigger_type": rule.trigger_type,
            }

        if rule.trigger_type == "days_without_record":
            return self._evaluate_days_without_record(db, user_id, rule)

        if rule.trigger_type == "recent_chat_keyword":
            return self._evaluate_recent_chat_keyword(db, user_id, rule)

        raise BusinessException(
            code=40063,
            message=f"unsupported trigger_type: {rule.trigger_type}",
            status_code=400,
        )

    def check_for_user(
        self,
        db: Session,
        rule_id: int,
        user_id: int,
    ) -> dict[str, Any]:
        rule = self.get_or_raise(db, rule_id)
        request_payload = {
            "rule_id": rule.id,
            "trigger_type": rule.trigger_type,
            "condition_json": rule.condition_json,
            "checked_at": datetime.now(UTC).isoformat(),
        }

        try:
            result = self.evaluate_for_user(db, user_id, rule)
            status = "triggered" if result["triggered"] else "not_triggered"
            log = active_log_service.create_log(
                db=db,
                user_id=user_id,
                trigger_rule_id=rule.id,
                action_type="rule_check",
                status=status,
                request_payload=request_payload,
                response_payload=result,
            )
            return {
                "log_id": log.id,
                "rule_id": rule.id,
                "user_id": user_id,
                "action_type": "rule_check",
                "status": status,
                "triggered": result["triggered"],
                "reason": result["reason"],
                "response_payload": result,
                "created_at": log.created_at,
            }
        except BusinessException as exc:
            active_log_service.create_log(
                db=db,
                user_id=user_id,
                trigger_rule_id=rule.id,
                action_type="rule_check",
                status="failed",
                request_payload=request_payload,
                response_payload={"error": exc.message},
            )
            raise

    def _evaluate_days_without_record(
        self,
        db: Session,
        user_id: int,
        rule: TriggerRule,
    ) -> dict[str, Any]:
        condition = rule.condition_json or {}
        days_without_record = int(condition.get("days_without_record", 0))
        record_type = str(condition.get("record_type", "")).strip()

        if days_without_record <= 0:
            raise BusinessException(
                code=40064,
                message="days_without_record must be greater than 0",
                status_code=400,
            )

        if not record_type:
            raise BusinessException(
                code=40065,
                message="record_type is required for days_without_record",
                status_code=400,
            )

        stmt = (
            select(Record)
            .where(
                Record.user_id == user_id,
                Record.record_type == record_type,
            )
            .order_by(Record.record_time.desc(), Record.id.desc())
            .limit(1)
        )
        last_record = db.scalar(stmt)

        cutoff_time = datetime.now(UTC) - timedelta(days=days_without_record)
        last_record_time = None
        if last_record is not None:
            last_record_time = self._as_utc_datetime(last_record.record_time)

        triggered = last_record_time is None or last_record_time < cutoff_time

        if last_record is None:
            reason = f"user has no {record_type} record yet"
        elif triggered:
            reason = f"last {record_type} record is older than {days_without_record} days"
        else:
            reason = f"user still has recent {record_type} record"

        return {
            "triggered": triggered,
            "reason": reason,
            "trigger_type": rule.trigger_type,
            "record_type": record_type,
            "days_without_record": days_without_record,
            "last_record_time": last_record_time.isoformat() if last_record_time else None,
        }

    def _evaluate_recent_chat_keyword(
        self,
        db: Session,
        user_id: int,
        rule: TriggerRule,
    ) -> dict[str, Any]:
        condition = rule.condition_json or {}
        raw_keywords = condition.get("keywords", [])
        keywords = [str(item).strip() for item in raw_keywords if str(item).strip()]
        recent_limit = int(condition.get("recent_limit", 10))

        if not keywords:
            raise BusinessException(
                code=40066,
                message="keywords cannot be empty",
                status_code=400,
            )

        if recent_limit <= 0:
            raise BusinessException(
                code=40067,
                message="recent_limit must be greater than 0",
                status_code=400,
            )

        stmt = (
            select(Message)
            .join(Conversation, Message.conversation_id == Conversation.id)
            .where(
                Conversation.user_id == user_id,
                Message.role == "user",
            )
            .order_by(Message.created_at.desc(), Message.id.desc())
            .limit(recent_limit)
        )
        recent_messages = list(db.scalars(stmt).all())

        matched_items: list[dict[str, Any]] = []
        for message in recent_messages:
            lowered_content = message.content.lower()
            for keyword in keywords:
                if keyword.lower() in lowered_content:
                    matched_items.append(
                        {
                            "keyword": keyword,
                            "message_id": message.id,
                        }
                    )

        matched_keywords = list(
            dict.fromkeys(item["keyword"] for item in matched_items)
        )
        matched_message_ids = list(
            dict.fromkeys(item["message_id"] for item in matched_items)
        )
        triggered = bool(matched_items)

        if triggered:
            reason = f"recent chat contains keywords: {', '.join(matched_keywords)}"
        else:
            reason = "recent chat does not contain configured keywords"

        return {
            "triggered": triggered,
            "reason": reason,
            "trigger_type": rule.trigger_type,
            "recent_limit": recent_limit,
            "matched_keywords": matched_keywords,
            "matched_message_ids": matched_message_ids,
        }


trigger_rule_service = TriggerRuleService()
