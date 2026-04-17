from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.core.exception import BusinessException
from app.core.response import success_response
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.record import (
    RecordCreate,
    RecordListData,
    RecordQueryParams,
    RecordRead,
    RecordType,
    RecordUpdate,
)
from app.services.record_service import record_service

router = APIRouter(prefix="/records", tags=["records"])


def get_record_query_params(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    record_type: RecordType | None = Query(default=None),
    start_time: datetime | None = Query(
        default=None,
        description="ISO8601，例如 2026-04-01T00:00:00Z",
    ),
    end_time: datetime | None = Query(
        default=None,
        description="ISO8601，例如 2026-04-10T23:59:59Z",
    ),
) -> RecordQueryParams:
    if start_time and end_time and start_time > end_time:
        raise BusinessException(
            code=40024,
            message="start_time cannot be greater than end_time",
            status_code=400,
        )

    return RecordQueryParams(
        page=page,
        page_size=page_size,
        record_type=record_type,
        start_time=start_time,
        end_time=end_time,
    )


@router.post(
    "",
    response_model=ApiResponse[RecordRead],
    status_code=status.HTTP_201_CREATED,
)
def create_record(
    payload: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    record = record_service.create_for_user(db, current_user.id, payload)
    return success_response(
        data=RecordRead.model_validate(record),
        message="record created",
    )


@router.get(
    "",
    response_model=ApiResponse[RecordListData],
)
def list_records(
    query: RecordQueryParams = Depends(get_record_query_params),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    items, total = record_service.list_for_user(db, current_user.id, query)
    total_pages = (total + query.page_size - 1) // query.page_size if total else 0

    return success_response(
        data=RecordListData(
            items=[RecordRead.model_validate(item) for item in items],
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=total_pages,
        ),
        message="success",
    )


@router.get(
    "/{record_id}",
    response_model=ApiResponse[RecordRead],
)
def get_record_detail(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    record = record_service.get_or_raise(db, current_user.id, record_id)
    return success_response(
        data=RecordRead.model_validate(record),
        message="success",
    )


@router.put(
    "/{record_id}",
    response_model=ApiResponse[RecordRead],
)
def update_record(
    record_id: int,
    payload: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    record = record_service.update_for_user(
        db=db,
        user_id=current_user.id,
        record_id=record_id,
        payload=payload,
    )
    # update_for_user里面已经实现了记录的验证是否为对应用户
    return success_response(
        data=RecordRead.model_validate(record),
        message="record updated",
    )


@router.delete(
    "/{record_id}",
    response_model=ApiResponse[None],
)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    record_service.delete_for_user(db, current_user.id, record_id)
    return success_response(message="record deleted")