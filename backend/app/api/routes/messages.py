from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.core.response import success_response
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.message import MessageCreate, MessageListData, MessageRead
from app.services.message_service import message_service

router = APIRouter(
    prefix="/conversations/{conversation_id}/messages",
    tags=["messages"],
)


@router.get(
    "",
    response_model=ApiResponse[MessageListData],
)
def list_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    messages = message_service.list_for_conversation(
        db, current_user.id, conversation_id
    )
    return success_response(
        data=MessageListData(
            items=[MessageRead.model_validate(item) for item in messages]
        ),
        message="success",
    )


@router.post(
    "/debug",
    response_model=ApiResponse[MessageRead],
    status_code=status.HTTP_201_CREATED,
)
def create_message_debug(
    conversation_id: int,
    payload: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    message = message_service.create_debug_for_conversation(
        db=db,
        user_id=current_user.id,
        conversation_id=conversation_id,
        payload=payload,
    )
    return success_response(
        data=MessageRead.model_validate(message),
        message="message created",
    )