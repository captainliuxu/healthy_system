from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.timezone import now_beijing
from app.models.active_log import ActiveLog
from app.models.proactive_message import ProactiveMessage
from app.models.trigger_rule import TriggerRule
from app.services.active_log_service import active_log_service
from app.services.proactive_message_service import proactive_message_service
from app.services.proactive_window_service import proactive_window_service
from app.services.trigger_rule_service import trigger_rule_service
from app.ws.manager import realtime_manager


class ProactiveService:
    def execute_rule_for_user(
        self,
        db: Session,
        user_id: int,
        rule_id: int,
    ) -> dict[str, Any]:
        rule = trigger_rule_service.get_or_raise(db, rule_id)
        request_payload = {
            "rule_id": rule.id,
            "trigger_type": rule.trigger_type,
            "condition_json": rule.condition_json,
            "executed_at": now_beijing().isoformat(),
        }

        try:
            evaluation = trigger_rule_service.evaluate_for_user(db, user_id, rule)

            if not evaluation["triggered"]:
                log = active_log_service.create_log(
                    db=db,
                    user_id=user_id,
                    trigger_rule_id=rule.id,
                    action_type="generate_proactive_message",
                    status="skipped",
                    request_payload=request_payload,
                    response_payload=evaluation,
                )
                return {
                    "log_id": log.id,
                    "rule_id": rule.id,
                    "triggered": False,
                    "message_created": False,
                    "status": "skipped",
                    "reason": evaluation["reason"],
                    "proactive_message": None,
                }

            window = proactive_window_service.get_or_create_for_user(db, user_id)
            allowed, window_reason = proactive_window_service.allow_trigger_now(window)

            if not allowed:
                response_payload = {
                    **evaluation,
                    "window_reason": window_reason,
                    "quiet_hours_start": window.quiet_hours_start,
                    "quiet_hours_end": window.quiet_hours_end,
                }
                log = active_log_service.create_log(
                    db=db,
                    user_id=user_id,
                    trigger_rule_id=rule.id,
                    action_type="generate_proactive_message",
                    status="blocked",
                    request_payload=request_payload,
                    response_payload=response_payload,
                )
                return {
                    "log_id": log.id,
                    "rule_id": rule.id,
                    "triggered": True,
                    "message_created": False,
                    "status": "blocked",
                    "reason": window_reason,
                    "proactive_message": None,
                }

            today_count = self.count_today_created(db, user_id)
            if today_count >= window.max_trigger_per_day:
                response_payload = {
                    **evaluation,
                    "today_count": today_count,
                    "max_trigger_per_day": window.max_trigger_per_day,
                }
                log = active_log_service.create_log(
                    db=db,
                    user_id=user_id,
                    trigger_rule_id=rule.id,
                    action_type="generate_proactive_message",
                    status="rate_limited",
                    request_payload=request_payload,
                    response_payload=response_payload,
                )
                return {
                    "log_id": log.id,
                    "rule_id": rule.id,
                    "triggered": True,
                    "message_created": False,
                    "status": "rate_limited",
                    "reason": "max trigger per day exceeded",
                    "proactive_message": None,
                }

            title, content = self.build_message_content(rule, evaluation)
            proactive_message = proactive_message_service.create_message(
                db=db,
                user_id=user_id,
                trigger_rule=rule,
                title=title,
                content=content,
            )

            delivered_connection_count = self._push_created_message(
                user_id=user_id,
                proactive_message=proactive_message,
            )

            response_payload = {
                **evaluation,
                "proactive_message_id": proactive_message.id,
                "title": proactive_message.title,
                "status": proactive_message.status,
                "realtime_delivered_connection_count": delivered_connection_count,
            }
            log = active_log_service.create_log(
                db=db,
                user_id=user_id,
                trigger_rule_id=rule.id,
                action_type="generate_proactive_message",
                status="created",
                request_payload=request_payload,
                response_payload=response_payload,
            )
            return {
                "log_id": log.id,
                "rule_id": rule.id,
                "triggered": True,
                "message_created": True,
                "status": "created",
                "reason": evaluation["reason"],
                "proactive_message": proactive_message,
            }
        except Exception as exc:
            active_log_service.create_log(
                db=db,
                user_id=user_id,
                trigger_rule_id=rule.id,
                action_type="generate_proactive_message",
                status="failed",
                request_payload=request_payload,
                response_payload={"error": str(exc)},
            )
            raise

    def count_today_created(
        self,
        db: Session,
        user_id: int,
    ) -> int:
        day_start = now_beijing().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        stmt = (
            select(func.count())
            .select_from(ActiveLog)
            .where(
                ActiveLog.user_id == user_id,
                ActiveLog.action_type == "generate_proactive_message",
                ActiveLog.status == "created",
                ActiveLog.created_at >= day_start,
            )
        )
        return db.scalar(stmt) or 0

    def build_message_content(
        self,
        rule: TriggerRule,
        evaluation: dict[str, Any],
    ) -> tuple[str, str]:
        if rule.trigger_type == "days_without_record":
            return self._build_days_without_record_message(evaluation)

        if rule.trigger_type == "recent_chat_keyword":
            return self._build_recent_chat_keyword_message(evaluation)

        return (
            "主动关怀提醒",
            "系统检测到你可能需要一次健康关注，你可以打开应用查看建议。",
        )

    def _build_days_without_record_message(
        self,
        evaluation: dict[str, Any],
    ) -> tuple[str, str]:
        record_type = str(evaluation.get("record_type", "健康数据"))
        days_without_record = int(evaluation.get("days_without_record", 1))
        record_label = self._record_type_label(record_type)

        title = "健康记录提醒"
        content = (
            f"我注意到你已经 {days_without_record} 天没有记录{record_label}了。"
            "如果今天方便，可以补记一条；如果最近状态有波动，也建议尽快测一次。"
        )
        return title, content

    def _build_recent_chat_keyword_message(
        self,
        evaluation: dict[str, Any],
    ) -> tuple[str, str]:
        keywords = evaluation.get("matched_keywords") or []
        keyword_text = "、".join(str(item) for item in keywords) or "当前困扰"

        title = "健康关怀提示"
        content = (
            f"我注意到你最近的表达里出现了“{keyword_text}”相关内容。"
            "如果你愿意，可以继续说说现在最困扰你的点，我会先帮你整理成几个可执行的小建议。"
        )
        return title, content

    def _record_type_label(self, record_type: str) -> str:
        mapping = {
            "blood_pressure": "血压",
            "blood_glucose": "血糖",
            "sleep": "睡眠",
            "medication": "用药",
            "mood": "情绪",
            "checkin": "健康打卡",
        }
        return mapping.get(record_type, record_type)

    def _push_created_message(
        self,
        user_id: int,
        proactive_message: ProactiveMessage,
    ) -> int:
        payload = self.build_created_event_payload(proactive_message)
        return realtime_manager.send_json_to_user_sync(user_id, payload)

    def build_created_event_payload(
        self,
        proactive_message: ProactiveMessage,
    ) -> dict[str, Any]:
        return {
            "event": "proactive_message_created",
            "data": {
                "id": proactive_message.id,
                "user_id": proactive_message.user_id,
                "trigger_rule_id": proactive_message.trigger_rule_id,
                "trigger_type": proactive_message.trigger_type,
                "title": proactive_message.title,
                "content": proactive_message.content,
                "status": proactive_message.status,
                "created_at": proactive_message.created_at.isoformat(),
                "displayed_at": (
                    proactive_message.displayed_at.isoformat()
                    if proactive_message.displayed_at
                    else None
                ),
            },
        }

    def list_pending_created_event_payloads(
        self,
        db: Session,
        user_id: int,
    ) -> list[dict[str, Any]]:
        pending_messages = proactive_message_service.list_pending_for_user(db, user_id)
        return [
            self.build_created_event_payload(message)
            for message in pending_messages
        ]


proactive_service = ProactiveService()
