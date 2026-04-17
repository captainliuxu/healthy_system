from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.core.response import success_response
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate
from app.services.profile_service import profile_service

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post(
    "/me",
    response_model=ApiResponse[ProfileRead],
    status_code=status.HTTP_201_CREATED,
)
def create_my_profile(
    payload: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    profile = profile_service.create_for_user(db, current_user.id, payload)
    return success_response(
        data=ProfileRead.model_validate(profile),
        message="profile created",
    )


@router.get(
    "/me",
    response_model=ApiResponse[ProfileRead],
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    profile = profile_service.get_or_raise(db, current_user.id)
    return success_response(
        data=ProfileRead.model_validate(profile),
        message="success",
    )


@router.put(
    "/me",
    response_model=ApiResponse[ProfileRead],
)
def update_my_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    profile = profile_service.update_for_user(db, current_user.id, payload)
    return success_response(
        data=ProfileRead.model_validate(profile),
        message="profile updated",
    )