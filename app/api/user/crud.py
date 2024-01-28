from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.user.model import User
from app.api.user.schema import UserGet, UserCreate
from app.api.exception.handler import alchemy_error_handler
from app.common import dictionary_util
from app.configs.log import logger


class UserCrudError(Exception):
    pass


class UserCRUD:
    """
    User Model에 대한 CURD 구현 클래스
    """

    def __init__(self, session: Session):
        """
        생성자
        :param session: DB Session 객체
        """
        self.session = session

    @alchemy_error_handler(err_label="Crud Create error", err_class=UserCrudError)
    def create(self, user: UserCreate) -> User:
        """
        User 객체 생성
        :param user: 추가하려는 User 객체
        :return: model.User
        """
        insert_data = User(**dict(user))
        self.session.add(insert_data)
        self.session.commit()

        return insert_data

    @alchemy_error_handler(err_label="Crud Get error", err_class=UserCrudError)
    def get(self, user: UserGet) -> User:
        """
        User 객체를 가져오기
        :param user: user 요청 객체
        :return: model.User
        """
        return self.session \
            .query(User) \
            .filter(User.id == user.id) \
            .first()

    @alchemy_error_handler(err_label="Crud Update error", err_class=UserCrudError)
    def update(self, update_data: UserGet) -> None:
        """
        User 객체 수정
        :param update_data: 수정하려는 데이터
        :return: None
        """
        # 값이 None인 키 삭제
        filtered_dict = dictionary_util.remove_none(dict(update_data))
        updated = self.session.query(User) \
            .filter(User.id == update_data.id) \
            .update(filtered_dict)
        self.session.commit()

        if updated == 0:
            logger.error(f"[User]Update is None. id : {update_data.id}")

    @alchemy_error_handler(err_label="Crud Delete error", err_class=UserCrudError)
    def delete(self, user: UserGet) -> None:
        """
        User 삭제
        :param user: 삭제 요청 객체
        :return: None
        """
        deleted = self.session.query(User) \
            .filter(User.id == user.id) \
            .update({"deleted": True})
        self.session.commit()

        if deleted == 0:
            logger.error(f"[User]Delete is None. id : {user.id}")
