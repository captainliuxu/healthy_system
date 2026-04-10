from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.core.response import success_response
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=ApiResponse[UserRead],
)
def get_me(
    current_user: User = Depends(get_current_active_user),
):
    return success_response(
        data=UserRead.model_validate(current_user),
        message="success",
    )


@router.put(
    "/me",
    response_model=ApiResponse[UserRead],
)
def update_me(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user = user_service.update_basic_info(db, current_user, payload)
    return success_response(
        data=UserRead.model_validate(user),
        message="update success",
    )