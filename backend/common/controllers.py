import string

from werkzeug.security import generate_password_hash, check_password_hash

from bson.errors import InvalidId
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
        try:
            return self._user_worker.get_by_id(ObjectId(user_id))
        except InvalidId:
            pass

    def get_user_by_username(self, username):
        return self._user_worker.get_by_username(username)

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
            try:
                return workers.UserLogin(self._user_worker.get_by_id(ObjectId(user_id)))
            except InvalidId:
                pass
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
            name=cleaners.TitleCleaner.clean(name),
            surname=cleaners.TitleCleaner.clean(surname)
        )
        user_login = None
        if user:
            user_login = workers.UserLogin(user)
        return user_login


class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
        self._project_worker = workers.ProjectWorker()
        self._user_worker = workers.UserWorker()
        self._pp_worker = workers.ProjectParticipantWorker()

    def get_project(self, project_id):
        try:
            return self._project_worker.get_by_id(ObjectId(project_id))
        except InvalidId:
            pass

    def check_title_free(self, title: str) -> bool:
        return not self._project_worker.get_by_title(cleaners.TitleCleaner.clean(title))

    @staticmethod
    def validate_title(title):
        return validators.TitleValidator().check_validation(title)

    def create_project(self, title):
        return self._project_worker.add_project(cleaners.TitleCleaner.clean(title))

    def find_project_by_title(self, title_match):
        return self._project_worker.get_by_title_like(cleaners.TitleCleaner.clean(title_match))

    def _update_head(self, pp):
        if pp.project.head:
            self._pp_worker.update_role(pp.project.head.id, consts.RoleEnum.worker)

        self._project_worker.set_head(pp.id, pp.project.id)
        return self._pp_worker.update_role(pp.id, consts.RoleEnum.head)

    def add_user_to_project(self, user_id, project_id, role=consts.RoleEnum.worker):
        project_id, user_id = ObjectId(project_id), ObjectId(user_id)
        project = self._project_worker.get_by_id(project_id)
        user = self._user_worker.get_by_id(user_id)
        if user and project:
            pp = self._pp_worker.create_pp(user_id, project_id, role)
            if pp:
                pp.project = self._project_worker.add_participant(
                    project_id,
                    pp.id,
                    as_head=role == consts.RoleEnum.head)
                pp.user = self._user_worker.add_project(user_id, pp.id)
                if pp.project and pp.user:
                    pp.project.head = pp
                    pp.project.participants.remove(pp.id)
                    pp.project.participants.append(pp)
                    pp.user.projects.remove(pp.id)
                    pp.user.projects.append(pp)
                    return pp
                self.logger.error(f'Error occurred with project participant id {pp.id}')


    def set_head(self, project_id, user_id):
        project_id, user_id = ObjectId(project_id), ObjectId(user_id)
        user = self._user_worker.get_by_id(user_id)
        project = self._project_worker.get_by_id(project_id)
        if user and project:
            pp = self._pp_worker.get_by_project_id_and_user_id(project_id, user_id)
            if pp and pp.role != consts.RoleEnum.head:
                pp = self._update_head(pp)
            elif not pp:
                pp = self.add_user_to_project(user_id, project_id, consts.RoleEnum.head)
            return pp

