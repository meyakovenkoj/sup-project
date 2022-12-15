import string

from werkzeug.security import generate_password_hash, check_password_hash

from bson.errors import InvalidId
from bson.objectid import ObjectId

from common.logger import get_logger
from common import workers, consts, validators, cleaners, base
from common import file_worker as fw


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

    def get_project_by_title(self, title):
        return self._project_worker.get_by_title(cleaners.TitleCleaner.clean(title))

    def find_project_by_title(self, title_match):
        return self._project_worker.get_by_title_like(cleaners.TitleCleaner.clean(title_match))

    def _update_head(self, pp):
        if pp.project.head:
            self._pp_worker.update_role(pp.project.head.id, consts.RoleEnum.worker)

        self._project_worker.set_head(pp.id, pp.project.id)
        return self._pp_worker.update_role(pp.id, consts.RoleEnum.head)

    def add_user_to_project(self, user_id, project_id, role=consts.RoleEnum.worker):
        try:
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
        except InvalidId:
            pass

    def user_in_project(self, project_id, user_id):
        try:
            project_id, user_id = ObjectId(project_id), ObjectId(user_id)
            pp = self._pp_worker.get_by_project_id_and_user_id(project_id, user_id)
            return pp
        except InvalidId:
            pass

    def is_project_head(self, project_id, user_id):
        pp = self.user_in_project(project_id, user_id)
        return pp and pp.role == consts.RoleEnum.head

    def set_head(self, project_id, user_id):
        try:
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
        except InvalidId:
            pass

    def has_action_rights(self, project, user, action: consts.ProjectAction):
        """This method does not check project status, only roles"""
        if user.is_admin:
            return True
        pp = self._pp_worker.get_by_project_id_and_user_id(project.id, user.id)
        if pp and action == consts.ProjectAction.finish and pp.role == consts.RoleEnum.head:
            return True
        return False

    def perform_action(self, project, user_id, action: consts.ProjectAction):
        try:
            user_id = ObjectId(user_id)
            user = self._user_worker.get_by_id(user_id)
            if not self.has_action_rights(project, user, action):
                return False
        except InvalidId:
            pass

        if action == consts.ProjectAction.finish:
            if project.status != consts.ProjectStatus.open:
                return False
            # TODO: send notification
            project = self._project_worker.set_status(consts.ProjectStatus.closed, project.id)
        elif action == consts.ProjectAction.archive:
            if project.status != consts.ProjectStatus.closed:
                return False
            project = self._project_worker.set_status(consts.ProjectStatus.archived, project.id)
        elif action == consts.ProjectAction.reopen:
            if project.status != consts.ProjectStatus.archived:
                return False
            project = self._project_worker.set_status(consts.ProjectStatus.open, project.id)

        return project


class TaskController(BaseController):
    def __init__(self):
        super().__init__()
        self._task_worker = workers.TaskWorker()
        self._ts_worker = workers.TaskSubscriberWorker()
        self._project_worker = workers.ProjectWorker()
        # self._user_worker = workers.UserWorker()
        self._pp_worker = workers.ProjectParticipantWorker()

    def get_task(self, task_id):
        try:
            return self._task_worker.get_by_id(ObjectId(task_id))
        except InvalidId:
            pass

    def attach_files(self, task_id, upload_to):
        task = self.get_task(task_id)
        if task:
            attachment_info = fw.FileWorker(task).make(from_folder=upload_to)
            return self._task_worker.update_attachments(task.id, attachment_info)

    def check_title_free(self, title: str) -> bool:
        return not self._task_worker.get_by_title(cleaners.TitleCleaner.clean(title))

    @staticmethod
    def validate_data(title, description):
        return (
                validators.TitleValidator().check_validation(title) and
                validators.DescriptionValidator().check_validation(description)
        )

    def create_task(self, title, description, task_type, project_id, author_id):
        try:
            project_id = ObjectId(project_id)
            author_id = ObjectId(author_id)
            task = self._task_worker.add_task(
                title=cleaners.TitleCleaner.clean(title),
                description=cleaners.TextCleaner.clean(description),
                project_id=project_id,
                author_id=author_id,
                task_type=task_type
            )
            if task:
                project = self._project_worker.add_task(project_id, task.id)
                if project:
                    ts = self._ts_worker.create_ts(task.id, author_id)
                    author = self._pp_worker.add_subscription(author_id, ts.id)
                    task = self._task_worker.add_subscriber(task.id, ts.id)
                    ts.task = task
                    ts.subscriber = author
                    if task and ts and author:
                        return ts
        except InvalidId:
            pass
