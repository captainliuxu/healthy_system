from __future__ import annotations

import asyncio
from collections import defaultdict
from threading import Lock
from typing import Any

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[int, set[WebSocket]] = defaultdict(set)
        self._lock = Lock()
        self._loop: asyncio.AbstractEventLoop | None = None

    def bind_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        with self._lock:
            self._connections[user_id].add(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket) -> None:
        with self._lock:
            sockets = self._connections.get(user_id)
            if not sockets:
                return

            sockets.discard(websocket)
            if not sockets:
                self._connections.pop(user_id, None)

    async def send_json_to_user(
        self,
        user_id: int,
        payload: dict[str, Any],
    ) -> int:
        with self._lock:
            sockets = list(self._connections.get(user_id, set()))

        delivered_count = 0
        broken_sockets: list[WebSocket] = []

        for websocket in sockets:
            try:
                await websocket.send_json(payload)
                delivered_count += 1
            except Exception:
                broken_sockets.append(websocket)

        for websocket in broken_sockets:
            self.disconnect(user_id, websocket)

        return delivered_count

    def send_json_to_user_sync(
        self,
        user_id: int,
        payload: dict[str, Any],
        timeout: float = 5,
    ) -> int:
        if self._loop is None or self._loop.is_closed():
            return 0

        future = asyncio.run_coroutine_threadsafe(
            self.send_json_to_user(user_id, payload),
            self._loop,
        )
        try:
            return future.result(timeout=timeout)
        except Exception:
            return 0

    def count_for_user(self, user_id: int) -> int:
        with self._lock:
            return len(self._connections.get(user_id, set()))

    def reset(self) -> None:
        with self._lock:
            self._connections.clear()
        self._loop = None


realtime_manager = ConnectionManager()