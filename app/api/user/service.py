from sqlalchemy.orm import Session

from app.api.user.crud import UserCRUD, UserCrudError
from app.api.user.schema import UserCreate, UserGet, UserAllGet, UserStatus
from app.common.passwd_util import PasswdUtil
from app.api.exception import api_error
from app.configs.log import logger


class UserService:
    """
    User 서비스 로직을 구현한 클래스
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate) -> None:
        try:
            result = UserCRUD(self.db).get(user=UserGet(id=user.id))
        except UserCrudError:
            logger.error(f"[UserService] UserCRUD get error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        if result:
            logger.error(f"[UserService] user[{user.id}] is already existed")
            raise api_error.AlreadyExistedUser(user_id=user.id)

        create_data = user
        create_data.pw = PasswdUtil.get_hash(password=user.pw)

        try:
            created_user = UserCRUD(self.db).create(user=create_data)
        except UserCrudError:
            logger.error(f"[UserService] UserCRUD create error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

    def get(self, user_id: str):
        """
        User 가져오기
        :param user_id: 사용자 아이디
        :return: User
        """
        try:
            user = UserCRUD(self.db).get(UserGet(id=user_id))
        except UserCrudError:
            logger.error(f"[UserService] UserCRUD get error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        if not user:
            logger.error(f"[UserService] user[{user_id}] is not found")
            raise api_error.UserNotFound(user_id=user_id)

        return UserAllGet(id=user.id, pw=user.pw, deleted=user.deleted)

    def get_status(self, user_id: str):
        """
        user 상태 정보 가져오기
        :param user_id: 사용자 아이디
        :return: User
        """
        try:
            user = UserCRUD(self.db).get(UserGet(id=user_id))
        except UserCrudError:
            logger.error(f"[UserService] UserCRUD get error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        if not user:
            logger.error(f"[UserService] user[{user_id}] is not found")
            raise api_error.UserNotFound(user_id=user_id)

        return UserStatus(id=user.id, deleted=user.deleted)

    def update(self, user: UserGet) -> None:
        """
        User 수정
        :param user: 수정할 사용자 정보
        :return: None
        """
        try:
            result = UserCRUD(self.db).get(user=user)
        except UserCrudError:
            logger.error(f"[UserService] user[{user.id}] is already existed")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        if not result:
            logger.error(f"[UserService] user[{user.id}] is not found")
            raise api_error.UserNotFound(user_id=user.id)

        try:
            UserCRUD(self.db).update(update_data=user)
        except UserCrudError:
            logger.error(f"[UserService] UserCRUD update error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

    def delete(self, user_id: str) -> None:
        """
        User 삭제
        :param user_id: 삭제할 사용자 아이디
        :return: None
        """
        try:
            result = UserCRUD(self.db).get(user=UserGet(id=user_id))
        except UserCrudError:
            logger.error(f"[UserService] UserCRUD get error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        if not result:
            raise api_error.UserNotFound(user_id=user_id)

        # 이후 유저와 관련된 항목이 있다면 먼저 삭제처리한 후 유저를 삭제 처리해야 함

        try:
            UserCRUD(self.db).delete(user=UserGet(id=user_id))
        except UserCrudError:
            logger.error(f"[UserService] UserCRUD delete error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")
