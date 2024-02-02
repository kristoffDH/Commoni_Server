from enum import Enum
from datetime import datetime, timedelta

from jose import jwt, JWTError

from app.configs.config import auth_config, token_config


class TokenType(str, Enum):
    """
    token 타입 정의를 위한 enum class
    """
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"
    PERMANENT = "PERMANENT"


class InvalidateTokenError(Exception):
    pass


class TokenSubKey:
    """token에서 사용할 sub의 key 이름을 정의한 class"""
    USER_ID = "user_id"
    EXPIRATION = "exp"
    TYPE = "type"


class Token:
    """JWT 토큰 클래스"""

    def __init__(self, token: str, secret_key: str, algorithm: str):
        """토큰 생성자"""
        try:
            self.payload = jwt.decode(token=token, key=secret_key, algorithms=algorithm)
        except JWTError as err:
            raise InvalidateTokenError(err)

        self.token_string = token

    def is_expired(self, compare_timestamp: int) -> bool:
        """
        토큰의 만료일자를 파라미터와 비교하여 만료상태 확인
        PERMANENT Token은 만료일자가 없음으로 항상 False 반환
        :param compare_timestamp: 비교할 기준 시간(datetime의 timestamp값)
        :return: bool
        """
        if self.get_type() == TokenType.PERMANENT:
            return False

        expire = int(self.payload['exp'])
        return expire <= compare_timestamp

    def get_token(self) -> str:
        """
        토큰 원본 반환
        :return: str
        """
        return self.token_string

    def get_type(self) -> TokenType:
        """
        토큰 타입 확인
        :return: JwtTokenType
        """
        return TokenType(self.payload['type'])

    def get_data(self, key: str) -> str:
        """
        토큰의 만료일자를 제외한 데이터 가져오기.
        :param key: 찾으려는 데이터 키
        :return: str
        """
        return self.payload.get(key)


class TokenUtility:
    @staticmethod
    def create_from_token(token: str) -> Token:
        """
        토큰에서 JwtToken객체 생성
        :param token: 문자열로 된 토큰
        :return: Token
        """
        return Token(token, secret_key=auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM)

    @staticmethod
    def create_token(token_type: TokenType, token_info: dict) -> Token:
        """
        토큰 생성
        :param token_type: 생성할 토큰 타입
        :param token_info: 토큰에 추가할 데이터
        :return: Token
        """
        expire = TokenUtility.set_expiration(token_type)
        to_encode = {**expire, **token_info}
        try:
            token = jwt.encode(to_encode, auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM)
        except JWTError as err:
            raise InvalidateTokenError(err)

        return Token(token, secret_key=auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM)

    @staticmethod
    def set_expiration(token_type: TokenType):
        """
        토큰의 type을 기준으로 만료일자 생성
        :param token_type: 토큰 타입
        :return: dict
        """
        now = datetime.utcnow()
        match token_type:
            case TokenType.ACCESS:
                return {
                    TokenSubKey.EXPIRATION: now + timedelta(**token_config.ACCESS),
                    TokenSubKey.TYPE: TokenType.ACCESS
                }
            case TokenType.REFRESH:
                return {
                    TokenSubKey.EXPIRATION: now + timedelta(**token_config.REFRESH),
                    TokenSubKey.TYPE: TokenType.REFRESH
                }
            case _:
                return {TokenSubKey.TYPE: TokenType.PERMANENT}
