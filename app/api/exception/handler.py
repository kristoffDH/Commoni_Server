import functools

from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.exception.api_error import ApiErrorBase


async def base_exception_handler(_: Request, exc: ApiErrorBase):
    return JSONResponse(status_code=exc.http_status,
                        headers=exc.headers,
                        content=exc.make_content())


def error_handler(except_error, raise_error, handler_func, err_message):
    def wrapper(method):
        @functools.wraps(method)
        def _impl(self, *args, **kwargs):
            try:
                return method(self, *args, **kwargs)
            except except_error as err:
                handler_func(self, message=f"{err_message} - {err}")
                raise raise_error(err)

        return _impl

    return wrapper
