from typing import Any

from app.schemas.common import ApiResponse


def success_response(data: Any = None, message: str = "success") -> ApiResponse[Any]:
    return ApiResponse(code=0, message=message, data=data)


def error_response(code: int, message: str, data: Any = None) -> ApiResponse[Any]:
    return ApiResponse(code=code, message=message, data=data)