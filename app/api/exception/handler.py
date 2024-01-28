import functools

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.exception.api_error import ApiErrorBase
from app.configs.log import logger


def base_exception_handler(_: Request, exc: ApiErrorBase):
    return JSONResponse(status_code=exc.http_status,
                        headers=exc.headers,
                        content=exc.make_content())


def alchemy_error_handler(err_label, err_class):
    def wrapper(method):
        @functools.wraps(method)
        def _impl(self, *args, **kwargs):
            try:
                return method(self, *args, **kwargs)
            except SQLAlchemyError as err:
                logger.error(f"{err_label} : {err}")
                self.session.rollback()
                raise err_class(err)

        return _impl

    return wrapper
