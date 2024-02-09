from fastapi import FastAPI

from api.router import api_router
from api.exception.api_error import ApiErrorBase
from api.exception.handler import base_exception_handler

app = FastAPI(title="ComMoni")

app.include_router(router=api_router)

app.add_exception_handler(ApiErrorBase, base_exception_handler)
