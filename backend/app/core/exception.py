from fastapi import Request
from fastapi.responses import JSONResponse


class BusinessException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=400,
        content={"code": exc.code, "message": exc.message, "data": None},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"code": 50000, "message": "服务器内部错误", "data": None},
    )