from __future__ import annotations

import os
import sys
from datetime import timedelta
from pathlib import Path

from sqlalchemy import func, select

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.security import hash_password  # noqa: E402
from app.core.timezone import now_beijing  # noqa: E402
from app.db.session import Base, SessionLocal, engine  # noqa: E402
from app.models.conversation import Conversation  # noqa: E402
from app.models.message import Message  # noqa: E402
from app.models.profile import Profile  # noqa: E402
from app.models.proactive_window import ProactiveWindow  # noqa: E402
from app.models.record import Record  # noqa: E402
from app.models.trigger_rule import TriggerRule  # noqa: E402
from app.models.user import User  # noqa: E402

DEMO_USERNAME = os.getenv("DEMO_USERNAME", "demo_beijing")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "Demo123456")
DEMO_EMAIL = os.getenv("DEMO_EMAIL", "demo_beijing@example.com")
DEMO_PHONE = os.getenv("DEMO_PHONE", "13988880001")


def get_or_create_demo_user(db) -> User:
    user = db.scalar(select(User).where(User.username == DEMO_USERNAME))
    if user is None:
        user = User(
            username=DEMO_USERNAME,
            email=DEMO_EMAIL,
            phone=DEMO_PHONE,
            password_hash=hash_password(DEMO_PASSWORD),
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    user.email = DEMO_EMAIL
    user.phone = DEMO_PHONE
    user.password_hash = hash_password(DEMO_PASSWORD)
    user.is_active = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_profile(db, user_id: int) -> Profile:
    profile = db.scalar(select(Profile).where(Profile.user_id == user_id))
    if profile is not None:
        return profile

    profile = Profile(
        user_id=user_id,
        name="北京演示用户",
        age=68,
        gender="male",
        height=170.0,
        weight=66.5,
        chronic_history="高血压",
        allergy_history="无",
        emergency_contact="家属 13988880002",
        remark="第九阶段验收演示账号",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def seed_records(db, user_id: int) -> list[Record]:
    records = list(
        db.scalars(
            select(Record)
            .where(Record.user_id == user_id)
            .order_by(Record.record_time.desc(), Record.id.desc())
        ).all()
    )
    if records:
        return records

    now = now_beijing()
    records = [
        Record(
            user_id=user_id,
            record_type="blood_pressure",
            value="126/82",
            unit="mmHg",
            record_time=now - timedelta(days=2),
            note="早晨测量",
        ),
        Record(
            user_id=user_id,
            record_type="sleep",
            value="7.5",
            unit="hour",
            record_time=now - timedelta(days=1, hours=1),
            note="睡眠正常",
        ),
        Record(
            user_id=user_id,
            record_type="mood",
            value="轻度焦虑",
            unit="level",
            record_time=now - timedelta(hours=6),
            note="下午情绪一般",
        ),
    ]
    db.add_all(records)
    db.commit()
    return records


def get_or_create_conversation(db, user_id: int) -> Conversation:
    conversation = db.scalar(
        select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.title == "第九阶段演示会话",
        )
    )
    if conversation is None:
        conversation = Conversation(
            user_id=user_id,
            title="第九阶段演示会话",
            status="active",
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    message_count = db.scalar(
        select(func.count())
        .select_from(Message)
        .where(Message.conversation_id == conversation.id)
    )
    if message_count:
        return conversation

    messages = [
        Message(
            conversation_id=conversation.id,
            role="user",
            content="我最近晚上有点睡不好，还会有一点焦虑。",
            message_type="text",
        ),
        Message(
            conversation_id=conversation.id,
            role="assistant",
            content="先别着急，我们可以先从作息和白天活动量一起看看。",
            message_type="text",
        ),
    ]
    db.add_all(messages)
    db.commit()
    return conversation


def get_or_create_trigger_rule(db) -> TriggerRule:
    rule = db.scalar(
        select(TriggerRule).where(TriggerRule.name == "演示-聊天焦虑关键词")
    )
    if rule is not None:
        return rule

    rule = TriggerRule(
        name="演示-聊天焦虑关键词",
        trigger_type="recent_chat_keyword",
        enabled=True,
        condition_json={"keywords": ["焦虑"], "recent_limit": 10},
        priority=10,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def get_or_create_window(db, user_id: int) -> ProactiveWindow:
    window = db.scalar(
        select(ProactiveWindow).where(ProactiveWindow.user_id == user_id)
    )
    if window is not None:
        return window

    window = ProactiveWindow(
        user_id=user_id,
        enabled=True,
        quiet_hours_start="22:00",
        quiet_hours_end="08:00",
        max_trigger_per_day=2,
    )
    db.add(window)
    db.commit()
    db.refresh(window)
    return window


def main() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        user = get_or_create_demo_user(db)
        profile = get_or_create_profile(db, user.id)
        records = seed_records(db, user.id)
        conversation = get_or_create_conversation(db, user.id)
        rule = get_or_create_trigger_rule(db)
        window = get_or_create_window(db, user.id)

        print("演示数据准备完成")
        print(f"用户名: {user.username}")
        print(f"密码: {DEMO_PASSWORD}")
        print(f"用户ID: {user.id}")
        print(f"档案ID: {profile.id}")
        print(f"记录数: {len(records)}")
        print(f"会话ID: {conversation.id}")
        print(f"触发规则ID: {rule.id}")
        print(f"主动窗口ID: {window.id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
