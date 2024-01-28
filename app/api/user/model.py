from sqlalchemy import Column, Boolean, String, Integer

from app.database.model_base import Base


class User(Base):
    """
        사용자 모델

        Attributes
            - no : 사용자 아이디 번호
            - user_id : 사용자 아이디
            - user_pw : 사용자 비밀번호
            - deleted : 사용자 삭제 여부
    """
    no = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(50), primary_key=True)
    pw = Column(String(256))
    deleted = Column(Boolean, default=False)
