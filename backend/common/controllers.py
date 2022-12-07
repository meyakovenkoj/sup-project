import string
from werkzeug.security import generate_password_hash, check_password_hash

from bson.objectid import ObjectId

from common.logger import get_logger
from common import workers
from common import consts


class BaseController:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)


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
        if not isinstance(username, str) or any(char not in string.ascii_letters + string.digits for char in username):
            return False

        if not isinstance(name, str) or not name.isalpha():
            return False

        if not isinstance(surname, str) or not surname.isalpha():
            return False

        if not isinstance(password, str) or \
                len(password) < consts.MIN_PASSWORD_LEN or \
                not any(char.isdigit() for char in password) or \
                not any(char.islower() for char in password) or \
                not any(char.isupper() for char in password) or \
                not any(char in string.punctuation for char in password):
            return False

        return True

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



class UserController(BaseController):
    def __init__(self):
        super().__init__()
        self._user_worker = workers.UserWorker()

