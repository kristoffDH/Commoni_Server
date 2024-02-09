from sqlalchemy.orm import Session
from fastapi import status, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from api.auth.service import AuthService
from database.session import get_session

API_VERSION = "v1"
API_NAME = "auth"

auth_router = APIRouter(prefix=f"/{API_VERSION}/{API_NAME}")


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_by_request_form(
        *,
        db_session: Session = Depends(get_session),
        form_data=Depends(OAuth2PasswordRequestForm)
) -> JSONResponse:
    """
    로그인 및 토큰 생성
    """
    user_id = form_data.username
    user_pw = form_data.password

    access_token, refresh_token = AuthService(db_session).login_with_passwd(user_id=user_id, user_pw=user_pw)

    return JSONResponse(content={
        "access_token": access_token,
        "refresh_token": refresh_token
    })
