from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.common.passwd_util import PasswdUtil
from app.api.auth.token_util import TokenUtility, Token, TokenType, TokenSubKey
from app.common.redis_util import RedisUtil

from app.api.user.service import UserService

from app.api.exception import api_error
from app.configs.log import logger
from app.configs.config import auth_config, token_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=auth_config.URL)


class AuthService:
    def __init__(self, db_session: Session = None):
        """
        AuthService 초기화
        :param db_session: 디비 세션
        """
        self.db_session = db_session

    def login_with_passwd(self, user_id: str, user_pw: str) -> tuple:
        """
        로그인 사용자 인증
        :param user_id: 사용자 아이디
        :param user_pw: 사용자 비밀번호
        :return: tuple(access_token, refresh_token)
        """
        check_user = UserService(self.db_session).get(user_id=user_id)
        if not PasswdUtil.verify(plain=user_pw, hashed=check_user.pw):
            logger.error(f"[auth-service] user password is invalid")
            raise api_error.Unauthorized("password is invalid")

        access_token = AuthService.create_access_token(user_id=user_id)
        refresh_token = AuthService.create_refresh_token(user_id=user_id)

        return access_token.get_token(), refresh_token.get_token()

    def verify_token(self, token_value: str = Depends(oauth2_scheme)) -> Token:
        """
        토큰 검증
        :param token_value: 토큰 값
        :return: token
        """
        token = TokenUtility.create_from_token(token_value)
        compare_datetime = int(datetime.utcnow())
        if token.is_expired(compare_datetime):
            raise api_error.Unauthorized(message="token is expired...")

        user_id = token.get_data(TokenSubKey.USER_ID)
        UserService(self.db_session).get(user_id=user_id)
        return token

    def renew_token(self) -> tuple:
        """
        토큰 갱신
        :param token_value: refresh 토큰 값
        :return: tuple(access_token, refresh_token)
        """
        token = self.verify_token()
        if token.get_type() is not TokenType.REFRESH:
            raise api_error.Unauthorized(message="token is invalid")

        user_id = token.get_data(TokenSubKey.USER_ID)
        refresh_token = None
        compare_datetime = int(datetime.utcnow() + timedelta(days=token_config.CEHCK_BEFORE_DATE))

        if token.is_expired(compare_datetime):
            logger.info("[auth-service] refresh token's expiration date is approaching. Renew the token")
            refresh_token = self.create_refresh_token(user_id=user_id)

        access_token = self.create_access_token(user_id=user_id)
        return access_token, refresh_token

    @staticmethod
    def create_access_token(user_id: str) -> Token:
        """
        Access Token 생성
        :param user_id: 사용자 아이디
        :return: Token
        """
        return TokenUtility.create_token(
            token_type=TokenType.ACCESS,
            token_info={TokenSubKey.USER_ID: user_id}
        )

    @staticmethod
    def create_refresh_token(user_id: str) -> Token:
        """
        Refresh Token 생성
        :param user_id: 사용자 아이디
        :return: Token
        """
        return TokenUtility.create_token(
            token_type=TokenType.REFRESH,
            token_info={TokenSubKey.USER_ID: user_id}
        )

    @staticmethod
    def create_permanent_token(user_id: str) -> Token:
        """
        Permanent Token 생성
        :param user_id: 사용자 아이디
        :return: Token
        """
        return TokenUtility.create_token(
            token_type=TokenType.PERMANENT,
            token_info={TokenSubKey.USER_ID: user_id}
        )
