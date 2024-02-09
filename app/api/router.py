from fastapi import APIRouter

from api.auth.router import auth_router

API_ROOT_ENDPOINT = "/api"

api_router = APIRouter(prefix=API_ROOT_ENDPOINT)

api_router.include_router(auth_router, tags=["auth"])
