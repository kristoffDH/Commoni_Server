from typing import Dict, Any
from fastapi import status
from starlette.exceptions import HTTPException


class ApiErrorBase(HTTPException):
    """
    API Exception 처리를 위한 베이스 클래스
    Attributes:
        - status : http status code
        - message : 상세 내용
    """
    status_code: int = None
    detail: str = None
    headers: Dict[str, Any] = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


def make_content(self) -> dict:
    """
    클라이언트로 전달할 응답용 content 생성
    :return:
    """
    return {"detail": self.detail}


class UserNotFound(ApiErrorBase):
    """
    User 가 없을때 처리할 예외 클래스
    """

    def __init__(self, user_id: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"user[{user_id}] is not existed."


class AlreadyExistedUser(ApiErrorBase):
    """
    User 가 이미 존재할 때 처리할 예외 클래스
    """

    def __init__(self, user_id: str):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = f"{user_id} is already existed."


class ItemNotFound(ApiErrorBase):
    """
    Get요청에 대한 결과값이 없을 때 처리할 예외 클래스
    """

    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Item not Found."


class Unauthorized(ApiErrorBase):
    """
    UNAUTHORIZED에 대한 예외 처리 클래스
    """

    def __init__(self, detail: str):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = f"Unauthorized : {detail}"


class CommanageNotFound(ApiErrorBase):
    """
    ComManage 가 없을때 처리할 예외 클래스
    """

    def __init__(self, host_id: int):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"ComManage[{host_id}] is not existed."


class ServerError(ApiErrorBase):
    """
    서버 내에서 오류가 발생 했을 때 처리할 예외 클래스
    """

    def __init__(self, err_detail: str):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = f"Server error. Internal err code : {err_detail}"


class TokenInvalidate(ApiErrorBase):
    """
    token validate credentials 예외처리 클래스
    """

    def __init__(self, err_detail: str):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = f"toekn invalidate : {err_detail}"
        self.headers = {"WWW-Authenticate": "Bearer"}
