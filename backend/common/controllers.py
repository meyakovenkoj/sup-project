import string

from werkzeug.security import generate_password_hash, check_password_hash

from bson.objectid import ObjectId

from common.logger import get_logger
from common import workers, consts, validators, cleaners


class BaseController:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)



class UserController(BaseController):
    def __init__(self):
        super().__init__()
        self._user_worker = workers.UserWorker()

    def get_user(self, user_id):
        return self._user_worker.get_by_id(ObjectId(user_id))

    def find_user_by_username(self, username_match):
        return self._user_worker.get_by_username_like(username_match)


class AuthorizationController(BaseController):
    def __init__(self):
        super().__init__()
        self._user_worker = workers.UserWorker()

    def login_user(self, username, password):
        user = self._user_worker.get_by_username(username)
        user_login = None
        if user and check_password_hash(user.password_hash, password):
            user_login = workers.UserLogin(user)
        return user_login

    def get_user(self, user_id):
        if user_id:
            return workers.UserLogin(self._user_worker.get_by_id(ObjectId(user_id)))
        return None

    def check_username_free(self, username):
        return not self._user_worker.get_by_username(username)

    @staticmethod
    def validate_creds(username, password, name, surname):
        name_validator = validators.NameValidator()

        return (
                name_validator.check_validation(name) and
                name_validator.check_validation(surname) and
                validators.UsernameValidator().check_validation(username) and
                validators.PasswordValidator().check_validation(password)
        )

    def register(self, username, password, name, surname):
        user = self._user_worker.create_user(
            username=username,
            password_hash=generate_password_hash(password),
            name=name,
            surname=surname
        )
        user_login = None
        if user:
            user_login = workers.UserLogin(user)
        return user_login


class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
        self._project_worker = workers.ProjectWorker()

    def check_title_free(self, title: str) -> bool:
        return not self._project_worker.get_by_title(cleaners.TitleCleaner.clean(title))

    @staticmethod
    def validate_title(title):
        if not isinstance(title, str) or any(char in string.punctuation for char in title):
            return False
        return True

    def create_project(self, title):
        return self._project_worker.add_project(cleaners.TitleCleaner.clean(title))

    def find_project_by_title(self, title_match):
        self._project_worker.get_by_title_like(title_match)

    def set_head(self, project_id, user_id):
        pass
