import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.response import error_response

logger = logging.getLogger(__name__)

# 业务异常。
# 适合场景:
# 用户不存在 档案不存在
# 记录状态不允许 重复提交
# example:raise BusinessException(code=40001, message="profile not found", status_code=404)
class BusinessException(Exception):
    def __init__(
        self,
        code: int,
        message: str,
        status_code: int = 400,
        data: Any = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data


def build_json_response(
    status_code: int,
    code: int,
    message: str,
    data: Any = None,
) -> JSONResponse:
    payload = error_response(code=code, message=message, data=data)
    return JSONResponse(status_code=status_code, content=payload.model_dump())


async def business_exception_handler(
    request: Request,
    exc: BusinessException,
) -> JSONResponse:
    return build_json_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        data=exc.data,
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "request error"

    error_code_map = {
        401: 40100,
        403: 40300,
        404: 40400,
    }
    code = error_code_map.get(exc.status_code, exc.status_code * 100)

    return build_json_response(
        status_code=exc.status_code,
        code=code,
        message=message,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    error_list = []
    for item in exc.errors():
        error_list.append(
            {
                "field": ".".join(str(part) for part in item.get("loc", [])),
                "message": item.get("msg", "invalid input"),
            }
        )

    return build_json_response(
        status_code=422,
        code=42200,
        message="request validation error",
        data=error_list,
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception("Unhandled exception: %s", exc)
    return build_json_response(
        status_code=500,
        code=50000,
        message="internal server error",
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)