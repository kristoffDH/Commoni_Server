from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """
        Attributes
            - user_id : 사용자 아이디
            - user_pw : 사용자 비밀번호
    """
    no: Optional[int] = None
    id: Optional[str] = None
    pw: Optional[str] = None
    deleted: Optional[bool] = None


class UserGet(UserBase):
    """User 객체를 가져올 때 사용"""
    id: str


class UserCreate(UserBase):
    """User 객체를 생성할 때 사용"""
    id: str
    pw: str


class UserStatus(UserBase):
    """User 객체의 상태 가져올 때 사용"""
    id: str
    deleted: bool


class UserAllGet(UserBase):
    """User 객체의 모든 값을 가져올 때 사용"""
    id: str
    pw: str
    deleted: bool
