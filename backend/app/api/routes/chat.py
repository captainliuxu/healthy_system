from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.core.response import success_response
from app.models.user import User
from app.schemas.chat import ChatSendData, ChatSendRequest
from app.schemas.common import ApiResponse
from app.services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "/send",
    response_model=ApiResponse[ChatSendData],
)
def send_chat_message(
    payload: ChatSendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = chat_service.send_message(
        db=db,
        user_id=current_user.id,
        payload=payload,
    )
    return success_response(
        data=result,
        message="chat reply generated",
    )