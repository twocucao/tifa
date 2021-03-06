import enum
from typing import Optional

from starlette.requests import Request
from starlette.responses import JSONResponse

from tifa.api import ApiResult


class HttpCodeEnum(enum.Enum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500


class BizCodeEnum(enum.Enum):
    # 业务状态码
    OK = "100200"
    FAIL = "100500"
    NOT_EXISTS = "100404"


error_message = {
    HttpCodeEnum.BAD_REQUEST.name: "错误请求",
    HttpCodeEnum.UNAUTHORIZED.name: "未授权",
    HttpCodeEnum.FORBIDDEN.name: "权限不足",
    HttpCodeEnum.NOT_FOUND.name: "未找到资源",
    HttpCodeEnum.SERVER_ERROR.name: "服务器异常",
    BizCodeEnum.FAIL: "未知错误",
}


class ApiException(Exception):
    status_code = HttpCodeEnum.BAD_REQUEST.value

    code: Optional[int]
    message: Optional[str] = None

    def __init__(self, message, status_code=None, biz_code=None, errors=None):
        # http status code
        self.status_code = status_code or self.status_code

        self.code = self.status_code or self.code
        self.biz_code = biz_code or self.biz_code
        self.message = message or self.message
        self.errors = errors or self.errors

    def to_result(self):
        rv = {"message": self.message}
        if self.code:
            rv["code"] = self.code
        if self.biz_code:
            rv["biz_code"] = self.biz_code
        if self.errors:
            rv["errors"] = self.errors
        return ApiResult(rv, status_code=self.status_code)


class NotAuthorized(ApiException):
    status_code = HttpCodeEnum.UNAUTHORIZED.value


class NotFound(ApiException):
    status_code = HttpCodeEnum.NOT_FOUND.value
    message = error_message[HttpCodeEnum.NOT_FOUND.name]


class InvalidToken(ApiException):
    status_code = HttpCodeEnum.UNAUTHORIZED.value


class AuthExpired(ApiException):
    status_code = HttpCodeEnum.UNAUTHORIZED.value


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )
