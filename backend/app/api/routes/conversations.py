from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.core.response import success_response
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.conversation import (
    ConversationCreate,
    ConversationListData,
    ConversationRead,
    ConversationTitleUpdate,
)
from app.services.conversation_service import conversation_service

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post(
    "",
    response_model=ApiResponse[ConversationRead],
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    payload: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    conversation = conversation_service.create_for_user(
        db, current_user.id, payload
    )
    return success_response(
        data=ConversationRead.model_validate(conversation),
        message="conversation created",
    )


@router.get(
    "",
    response_model=ApiResponse[ConversationListData],
)
def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    conversations = conversation_service.list_for_user(db, current_user.id)
    return success_response(
        data=ConversationListData(
            items=[
                ConversationRead.model_validate(item)
                for item in conversations
            ]
        ),
        message="success",
    )


@router.get(
    "/{conversation_id}",
    response_model=ApiResponse[ConversationRead],
)
def get_conversation_detail(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    conversation = conversation_service.get_or_raise(
        db, current_user.id, conversation_id
    )
    return success_response(
        data=ConversationRead.model_validate(conversation),
        message="success",
    )


@router.put(
    "/{conversation_id}/title",
    response_model=ApiResponse[ConversationRead],
)
def update_conversation_title(
    conversation_id: int,
    payload: ConversationTitleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    conversation = conversation_service.update_title_for_user(
        db=db,
        user_id=current_user.id,
        conversation_id=conversation_id,
        payload=payload,
    )
    return success_response(
        data=ConversationRead.model_validate(conversation),
        message="conversation title updated",
    )


@router.delete(
    "/{conversation_id}",
    response_model=ApiResponse[None],
)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    conversation_service.delete_for_user(db, current_user.id, conversation_id)
    return success_response(message="conversation deleted")