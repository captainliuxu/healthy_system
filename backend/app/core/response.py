from app.schemas.common import ApiResponse


def success_response(data=None, message: str = "success"):
    return ApiResponse(code=0, message=message, data=data)