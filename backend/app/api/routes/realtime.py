from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect

from app.api.deps import get_current_active_user
from app.core.config import settings
from app.core.exception import BusinessException
from app.core.response import success_response
from app.core.security import InvalidTokenError, decode_access_token
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.realtime import RealtimePushTestData, RealtimePushTestRequest
from app.services.proactive_service import proactive_service
from app.ws.manager import realtime_manager

router = APIRouter(prefix="/realtime", tags=["realtime"])


def authenticate_websocket_user(token: str) -> User:
    credentials_error = BusinessException(
        code=40100,
        message="invalid or expired token",
        status_code=401,
    )

    try:
        payload = decode_access_token(token)
    except InvalidTokenError:
        raise credentials_error

    user_id = payload.get("sub")
    if not user_id:
        raise credentials_error

    db = SessionLocal()
    try:
        user = db.get(User, int(user_id))
        if not user:
            raise credentials_error
        if not user.is_active:
            raise BusinessException(
                code=40300,
                message="inactive user",
                status_code=403,
            )
        return user
    finally:
        db.close()


def load_pending_proactive_events(user_id: int) -> list[dict]:
    db = SessionLocal()
    try:
        return proactive_service.list_pending_created_event_payloads(db, user_id)
    finally:
        db.close()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
):
    if not settings.WS_ENABLED:
        await websocket.close(code=1008, reason="websocket is disabled")
        return

    try:
        current_user = authenticate_websocket_user(token)
    except BusinessException as exc:
        await websocket.close(code=1008, reason=exc.message)
        return

    await realtime_manager.connect(current_user.id, websocket)
    await realtime_manager.send_json_to_user(
        current_user.id,
        {
            "event": "connected",
            "message": "realtime channel connected",
            "user_id": current_user.id,
            "connected_at": datetime.now(UTC).isoformat(),
        },
    )
    # Replay still-pending proactive messages so late WebSocket connections
    # can observe the same event stream after scheduler-generated creation.
    for payload in load_pending_proactive_events(current_user.id):
        await websocket.send_json(payload)

    try:
        while True:
            text = await websocket.receive_text()
            if text.strip().lower() == "ping":
                await websocket.send_json(
                    {
                        "event": "pong",
                        "message": "pong",
                        "sent_at": datetime.now(UTC).isoformat(),
                    }
                )
    except WebSocketDisconnect:
        realtime_manager.disconnect(current_user.id, websocket)
    except Exception:
        realtime_manager.disconnect(current_user.id, websocket)
        raise


@router.post(
    "/test-push/me",
    response_model=ApiResponse[RealtimePushTestData],
)
def send_test_push_to_current_user(
    payload: RealtimePushTestRequest,
    current_user: User = Depends(get_current_active_user),
):
    delivered_connection_count = realtime_manager.send_json_to_user_sync(
        current_user.id,
        {
            "event": "manual_test_push",
            "data": {
                "content": payload.content,
                "sent_at": datetime.now(UTC).isoformat(),
            },
        },
    )
    return success_response(
        data=RealtimePushTestData(
            event="manual_test_push",
            content=payload.content,
            delivered_connection_count=delivered_connection_count,
        ),
        message="realtime push sent",
    )
