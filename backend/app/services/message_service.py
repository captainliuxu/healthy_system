from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.models.message import Message
from app.schemas.message import MessageCreate
from app.services.conversation_service import conversation_service


class MessageService:
    def list_for_conversation(
        self,
        db: Session,
        user_id: int,
        conversation_id: int,
    ) -> list[Message]:
        conversation_service.get_or_raise(db, user_id, conversation_id)

        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc(), Message.id.asc())
        )
        return list(db.scalars(stmt).all())
    # 拿最近若干条历史消息，专门给大模型上下文使用。
    def get_recent_for_conversation(
        self,
        db: Session,
        user_id: int,
        conversation_id: int,
        limit: int = 10,
    ) -> list[Message]:
        conversation_service.get_or_raise(db, user_id, conversation_id)

        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc(), Message.id.desc())
            .limit(limit)
        )
        items = list(db.scalars(stmt).all())
        items.reverse()
        return items

    def create_for_conversation(
        self,
        db: Session,
        user_id: int,
        conversation_id: int,
        role: str,
        content: str,
        message_type: str = "text",
    ) -> Message:
        conversation = conversation_service.get_or_raise(
            db, user_id, conversation_id
        )

        cleaned_content = content.strip()
        if not cleaned_content:
            raise BusinessException(
                code=40041,
                message="content cannot be empty",
                status_code=400,
            )

        cleaned_message_type = message_type.strip()
        if not cleaned_message_type:
            raise BusinessException(
                code=40042,
                message="message_type cannot be empty",
                status_code=400,
            )

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=cleaned_content,
            message_type=cleaned_message_type,
        )

        db.add(message)

        conversation.updated_at = datetime.now(UTC)
        db.add(conversation)

        db.commit()
        db.refresh(message)
        return message

    def create_debug_for_conversation(
        self,
        db: Session,
        user_id: int,
        conversation_id: int,
        payload: MessageCreate,
    ) -> Message:
        return self.create_for_conversation(
            db=db,
            user_id=user_id,
            conversation_id=conversation_id,
            role=payload.role.value,
            content=payload.content,
            message_type=payload.message_type,
        )


message_service = MessageService()