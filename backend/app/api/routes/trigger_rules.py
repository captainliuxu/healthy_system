from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.core.response import success_response
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.trigger_rule import (
    TriggerRuleCheckData,
    TriggerRuleCreate,
    TriggerRuleListData,
    TriggerRuleRead,
    TriggerRuleUpdate,
)
from app.services.trigger_rule_service import trigger_rule_service

router = APIRouter(prefix="/trigger-rules", tags=["trigger-rules"])


@router.post(
    "",
    response_model=ApiResponse[TriggerRuleRead],
    status_code=status.HTTP_201_CREATED,
)
def create_trigger_rule(
    payload: TriggerRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    rule = trigger_rule_service.create(db, payload)
    return success_response(
        data=TriggerRuleRead.model_validate(rule),
        message="trigger rule created",
    )


@router.get(
    "",
    response_model=ApiResponse[TriggerRuleListData],
)
def list_trigger_rules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    items = trigger_rule_service.list_all(db)
    return success_response(
        data=TriggerRuleListData(
            items=[TriggerRuleRead.model_validate(item) for item in items]
        ),
        message="success",
    )


@router.get(
    "/{rule_id}",
    response_model=ApiResponse[TriggerRuleRead],
)
def get_trigger_rule_detail(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    rule = trigger_rule_service.get_or_raise(db, rule_id)
    return success_response(
        data=TriggerRuleRead.model_validate(rule),
        message="success",
    )


@router.put(
    "/{rule_id}",
    response_model=ApiResponse[TriggerRuleRead],
)
def update_trigger_rule(
    rule_id: int,
    payload: TriggerRuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    rule = trigger_rule_service.update(db, rule_id, payload)
    return success_response(
        data=TriggerRuleRead.model_validate(rule),
        message="trigger rule updated",
    )


@router.post(
    "/{rule_id}/check/me",
    response_model=ApiResponse[TriggerRuleCheckData],
)
def check_trigger_rule_for_current_user(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = trigger_rule_service.check_for_user(
        db=db,
        rule_id=rule_id,
        user_id=current_user.id,
    )
    return success_response(
        data=TriggerRuleCheckData.model_validate(result),
        message="rule checked",
    )