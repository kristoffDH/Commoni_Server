from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.exception.api_error import ApiErrorBase


def base_exception_handler(_: Request, exc: ApiErrorBase):
    return JSONResponse(status_code=exc.http_status,
                        headers=exc.headers,
                        content=exc.make_content())