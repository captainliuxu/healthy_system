from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate, ConversationTitleUpdate


class ConversationService:
    def create_for_user(
        self,
        db: Session,
        user_id: int,
        payload: ConversationCreate,
    ) -> Conversation:
        title = (payload.title or "").strip() or "New Conversation"

        conversation = Conversation(
            user_id=user_id,
            title=title,
            status="active",
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def list_for_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Conversation]:
        stmt = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc(), Conversation.id.desc())
        )
        return list(db.scalars(stmt).all())

    def get_or_raise(
        self,
        db: Session,
        user_id: int,
        conversation_id: int,
    ) -> Conversation:
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        conversation = db.scalar(stmt)
        if not conversation:
            raise BusinessException(
                code=40431,
                message="conversation not found",
                status_code=404,
            )
        return conversation

    def update_title_for_user(
        self,
        db: Session,
        user_id: int,
        conversation_id: int,
        payload: ConversationTitleUpdate,
    ) -> Conversation:
        conversation = self.get_or_raise(db, user_id, conversation_id)
        title = payload.title.strip()

        if not title:
            raise BusinessException(
                code=40031,
                message="title cannot be empty",
                status_code=400,
            )

        conversation.title = title
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def delete_for_user(
        self,
        db: Session,
        user_id: int,
        conversation_id: int,
    ) -> None:
        conversation = self.get_or_raise(db, user_id, conversation_id)

        db.execute(
            delete(Message).where(Message.conversation_id == conversation.id)
        )
        db.delete(conversation)
        db.commit()


conversation_service = ConversationService()