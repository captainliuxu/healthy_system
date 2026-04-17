from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.core.response import success_response
from app.models.user import User
from app.schemas.active_log import ActiveLogListData, ActiveLogRead
from app.schemas.common import ApiResponse
from app.services.active_log_service import active_log_service

router = APIRouter(prefix="/active-logs", tags=["active-logs"])


@router.get(
    "",
    response_model=ApiResponse[ActiveLogListData],
)
def list_active_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    items = active_log_service.list_for_user(db, current_user.id)
    return success_response(
        data=ActiveLogListData(
            items=[ActiveLogRead.model_validate(item) for item in items]
        ),
        message="success",
    )


@router.get(
    "/{log_id}",
    response_model=ApiResponse[ActiveLogRead],
)
def get_active_log_detail(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    log = active_log_service.get_or_raise(db, current_user.id, log_id)
    return success_response(
        data=ActiveLogRead.model_validate(log),
        message="success",
    )