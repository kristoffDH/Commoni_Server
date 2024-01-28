import pytest

from app.api.user.crud import UserCrudError
from app.api.user.service import UserService
from app.api.user.model import User
from app.api.user.schema import UserAllGet, UserStatus, UserGet, UserCreate

from app.api.exception import api_error


class TestUserService:
    id = "test_user"
    pw = "1234567890"

    user_data = {
        "id": id,
        "pw": pw,
    }

    user_model = User(id=id, pw=pw)
    user_get_schema = UserGet(id=id)
    user_create_schema = UserCreate(id=id, pw=pw)
    user_all_get_schema = UserAllGet(id=id, pw=pw, deleted=False)
    user_status_schema = UserStatus(id=id, deleted=False)

    def test_create_success(self, mocker):
        """
        유저 생성 테스트
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)
        mocker.patch('app.api.user.crud.UserCRUD.create', return_value=self.user_model)

        UserService(db).create(user=self.user_create_schema)

    def test_create_fail_1(self, mocker):
        """
        유저 생성 테스트 실패. DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = UserCrudError

        with pytest.raises(api_error.ServerError):
            UserService(db).create(user=self.user_create_schema)

    def test_create_fail_2(self, mocker):
        """
        유저 생성 테스트 실패. 이미 유저가 있는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_model)

        with pytest.raises(api_error.AlreadyExistedUser):
            UserService(db).create(user=self.user_create_schema)

    def test_create_fail_3(self, mocker):
        """
        유저 생성 테스트 실패. DB create error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)
        mocker.patch('app.api.user.crud.UserCRUD.create', return_value=self.user_model) \
            .side_effect = UserCrudError

        with pytest.raises(api_error.ServerError):
            UserService(db).create(user=self.user_create_schema)

    def test_get_success(self, mocker):
        """
        유저 정보 가져오기 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_all_get_schema)

        result = UserService(db).get(user_id=self.id)

        assert result == self.user_all_get_schema

    def test_get_fail_1(self, mocker):
        """
        유저 정보 가져오기 실패, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = UserCrudError

        with pytest.raises(api_error.ServerError):
            UserService(db).get(user_id=self.id)

    def test_get_fail_2(self, mocker):
        """
        유저 정보 가져오기 실패, 유저가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            UserService(db).get(user_id=self.id)

    def test_get_status_success(self, mocker):
        """
        유저 상태 정보 가져오기 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_status_schema)

        result = UserService(db).get_status(user_id=self.id)

        assert result == self.user_status_schema

    def test_get_status_fail_1(self, mocker):
        """
        유저 상태 정보 가져오기 실패, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = UserCrudError

        with pytest.raises(api_error.ServerError):
            UserService(db).get_status(user_id=self.id)

    def test_get_status_fail_2(self, mocker):
        """
        유저 상태 정보 가져오기 실패, 유저가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            UserService(db).get_status(user_id=self.id)

    def test_update_success(self, mocker):
        """
        유저 정보 업데이트 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_all_get_schema)

        UserService(db).update(user=self.user_get_schema)

    def test_update_fail_1(self, mocker):
        """
        유저 정보 업데이트 실패, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = UserCrudError

        with pytest.raises(api_error.ServerError):
            UserService(db).update(user=self.user_get_schema)

    def test_update_fail_2(self, mocker):
        """
        유저 정보 업데이트 실패, 유저가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            UserService(db).update(user=self.user_get_schema)

    def test_update_fail_3(self, mocker):
        """
        유저 정보 업데이트 실패, DB update error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_all_get_schema)
        mocker.patch('app.api.user.crud.UserCRUD.update', return_value=None) \
            .side_effect = UserCrudError

        with pytest.raises(api_error.ServerError):
            UserService(db).update(user=self.user_get_schema)

    def test_delete_success(self, mocker):
        """
        유저 삭제 성공,
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_all_get_schema)

        UserService(db).delete(user_id=self.id)

    def test_delete_fail_1(self, mocker):
        """
        유저 삭제 실패, 유저 get DB error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = UserCrudError

        with pytest.raises(api_error.ServerError):
            UserService(db).delete(user_id=self.id)

    def test_delete_fail_2(self, mocker):
        """
        유저 삭제 실패, 유저가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            UserService(db).delete(user_id=self.id)
