from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    """database 설정"""
    USER: str = "kristoff"
    PW: str = "1234"
    HOST: str = "localhost"
    PORT: int = 3306
    DB_NAME: str = "commonidb"
    URI: str = f'mysql+pymysql://{USER}:{PW}@{HOST}:{PORT}/{DB_NAME}'


class AuthConfig(BaseSettings):
    """인증 관련 설정"""
    SECRET_KEY: str = "0548a115e749bd446115d6c05e95838b2f7b47568e110186e0fe81fca376e19d"
    ALGORITHM: str = "HS256"
    URL: str = "/api/v1/auth/login"
    ACCESS_TOKEN_EXPIRATION: int = 20  # minute
    REFRESH_TOKEN_EXPIRATION: int = 15  # date
    DATE_BEFORE_EXPIRATION: int = 2  # date


class RedisConfig(BaseSettings):
    """Redis 관련 설"""
    REDIS_IP: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB_NUM: int = 0


db_config = DatabaseConfig()
auth_config = AuthConfig()
redis_confi = RedisConfig()
