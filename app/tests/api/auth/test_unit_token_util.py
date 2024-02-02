from datetime import datetime, timedelta, timezone

import pytest
from app.api.auth.token_util import TokenUtility, TokenSubKey, Token, TokenType, InvalidateTokenError

OTHER_SECRET_KEY: str = "0548a115e749bd446115d6c05e95838b2f7b47568e110186e0fe81fca376e1ff"
OTHER_ALGORITHM: str = "HS128"
EXPIRATION_ACCESS: dict = {'minutes': 20}
EXPIRATION_REFRESH: dict = {'days': 15}


class TestTokenUtil:
    user_id = "tester"

    def test_token_util_1(self):
        now = int(datetime.now(timezone.utc).timestamp())
        access_expiration_date = int((datetime.now(timezone.utc) + timedelta(**EXPIRATION_ACCESS)).timestamp())
        token_info = {TokenSubKey.USER_ID: self.user_id}

        token = TokenUtility.create_token(token_type=TokenType.ACCESS, token_info=token_info)

        assert token.get_type() == TokenType.ACCESS
        assert token.get_data(TokenSubKey.USER_ID) == self.user_id
        assert int(token.get_data(TokenSubKey.EXPIRATION)) <= access_expiration_date
        assert token.is_expired(now) is False

        TokenUtility.create_from_token(token=token.get_token())

    def test_token_util_2(self):
        """토큰 생성 테스트 Refresh"""
        now = int(datetime.now(timezone.utc).timestamp())
        refresh_expiration_date = int((datetime.now(timezone.utc) + timedelta(**EXPIRATION_REFRESH)).timestamp())
        token_info = {TokenSubKey.USER_ID: self.user_id}

        token = TokenUtility.create_token(token_type=TokenType.REFRESH, token_info=token_info)

        assert token.get_type() == TokenType.REFRESH
        assert token.get_data(TokenSubKey.USER_ID) == self.user_id
        assert int(token.get_data(TokenSubKey.EXPIRATION)) <= refresh_expiration_date
        assert token.is_expired(now) is False

        TokenUtility.create_from_token(token=token.get_token())

    def test_token_util_3(self):
        """토큰 생성 테스트 Permanent"""
        now = int(datetime.now(timezone.utc).timestamp())
        token_info = {TokenSubKey.USER_ID: self.user_id}

        token = TokenUtility.create_token(token_type=TokenType.PERMANENT, token_info=token_info)

        assert token.get_type() == TokenType.PERMANENT
        assert token.get_data(TokenSubKey.USER_ID) == self.user_id
        assert token.get_data(TokenSubKey.EXPIRATION) is None
        assert token.is_expired(now) is False

        TokenUtility.create_from_token(token=token.get_token())

    def test_token_util_4(self):
        """다른 SECRET_KEY로 토큰 객체를 만들려고 할경우 에러 발생"""
        token_info = {TokenSubKey.USER_ID: self.user_id}

        token = TokenUtility.create_token(token_type=TokenType.ACCESS, token_info=token_info)
        with pytest.raises(InvalidateTokenError):
            Token(token=token.get_token(), secret_key=OTHER_SECRET_KEY, algorithm=OTHER_ALGORITHM)
