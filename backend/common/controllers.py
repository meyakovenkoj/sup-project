import os.path
import string
import typing
import urllib.parse

from werkzeug.security import generate_password_hash, check_password_hash

from bson.errors import InvalidId
from bson.objectid import ObjectId

from common.logger import get_logger
from common import workers, consts, validators, cleaners, base
from common import file_worker as fw
from common.mailer import send_message
from common.conf import config


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

    def get_project_participant(self, pp_id):
        try:
            return self._pp_worker.get_by_id(ObjectId(pp_id))
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

    def get_user_projects(self, user_id):
        try:
            user_id = ObjectId(user_id)
            pps = self._pp_worker.get_by_user_id(user_id)
            return pps
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
            return False

        if action == consts.ProjectAction.finish:
            if project.status != consts.ProjectStatus.open:
                return False
            project = self._project_worker.set_status(consts.ProjectStatus.closed, project.id)
            __tc = TaskController()
            for task_id in project.tasks:
                __tc.notify_project_closing(task_id)
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
        self._user_worker = workers.UserWorker()
        self._pp_worker = workers.ProjectParticipantWorker()
        self._com_worker = workers.CommentWorker()
        self._task_actions: typing.Dict[consts.TaskAction, typing.Callable] = {
            consts.TaskAction.set_executor: self._set_executor,
            consts.TaskAction.set_tester: self._set_tester,
            consts.TaskAction.reopen: self._reopen,
            consts.TaskAction.verify: self._verify,
            consts.TaskAction.request_correction: self._request_correction,
            consts.TaskAction.finish: self._finish,
            consts.TaskAction.close: self._close,
        }

    def get_task(self, task_id):
        try:
            return self._task_worker.get_by_id(ObjectId(task_id))
        except InvalidId:
            pass

    def get_task_by_title(self, title):
        return self._task_worker.get_by_title(cleaners.TitleCleaner.clean(title))

    def find_task_by_title(self, title_match):
        return self._task_worker.get_by_title_like(cleaners.TitleCleaner.clean(title_match))

    def get_tasks_by_pp_id(self, pp_id):
        try:
            return self._task_worker.get_by_pp_assigned(ObjectId(pp_id))
        except InvalidId:
            pass

    def get_tasks_by_user_assignments(self, user_id):
        user = UserController().get_user(user_id)
        tasks = []
        if user:
            for pp in user.projects:
                pp_tasks = self._task_worker.get_by_pp_assigned(pp)
                if pp_tasks:
                    tasks.extend(pp_tasks)
        return tasks

    def attach_files(self, task_id, upload_to):
        task = self.get_task(task_id)
        if task:
            attachment_info = fw.FileWorker(task).make(from_folder=upload_to)
            return self._task_worker.update_attachments(task.id, attachment_info)

    def deattach_files(self, task_id, files):
        task = self.get_task(task_id)
        if task:
            attachment_info = fw.FileWorker(task).remove_files(files)
            if attachment_info is not None:
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

    def user_accessed_task(self, task_id, user_id):
        task = self.get_task(task_id)
        if task:
            return ProjectController().user_in_project(project_id=task.project, user_id=user_id)

    def subscribe_user_to_task(self, task_id, user_id):
        try:
            task_id = ObjectId(task_id)
            user_id = ObjectId(user_id)
            task = self._task_worker.get_by_id(task_id)
            if task:
                pp = self._pp_worker.get_by_project_id_and_user_id(task.project, user_id)
                if pp:
                    ts = self._ts_worker.get_by_task_id_and_project_participant_id(pp.id, task.id)
                    if ts:
                        return ts

                    ts = self._ts_worker.create_ts(task.id, pp.id)
                    pp = self._pp_worker.add_subscription(pp.id, ts.id)
                    task = self._task_worker.add_subscriber(task.id, ts.id)
                    ts.task = task
                    ts.subscriber = pp
                    if task and ts and pp:
                        return ts
        except InvalidId:
            pass

    def unsubscribe_user_from_task(self, task_id, user_id):
        try:
            task_id = ObjectId(task_id)
            user_id = ObjectId(user_id)
            task = self._task_worker.get_by_id(task_id)
            if task:
                pp = self._pp_worker.get_by_project_id_and_user_id(task.project, user_id)
                if pp:
                    ts = self._ts_worker.get_by_task_id_and_project_participant_id(pp.id, task.id)
                    if ts:
                        pp = self._pp_worker.remove_subscription(pp.id, ts.id)
                        task = self._task_worker.remove_subscriber(task.id, ts.id)
                        ts = self._ts_worker.remove_ts(ts.id)
                        if pp and task and ts:
                            return task
                        else:
                            return False
        except InvalidId:
            pass

    def validate_comment(self, text):
        return validators.DescriptionValidator().check_validation(text)

    def comment_task(self, task_id, user_id, text):
        try:
            user_id = ObjectId(user_id)
            user = self._user_worker.get_by_id(user_id)
        except InvalidId:
            return

        task = self.get_task(task_id)
        if user and task:
            pp = self._pp_worker.get_by_project_id_and_user_id(task.project, user.id)
            if pp:
                com = self._com_worker.create_comment(task.id, user.id, text=cleaners.TextCleaner().clean(text))
                if com:
                    return self._task_worker.add_comment(task.id, com.id)

    def get_comment(self, com_id):
        try:
            com_id = ObjectId(com_id)
            return self._com_worker.get_by_id(com_id)
        except InvalidId:
            pass

    def remove_comment(self, com_id):
        try:
            com_id = ObjectId(com_id)
            com = self._com_worker.get_by_id(com_id)
        except InvalidId:
            return

        if com:
            task = self._task_worker.remove_comment(com.task, com.id)
            if task:
                return self._com_worker.remove_comment(com.id)

    def edit_comment(self, com_id, new_text):
        try:
            com_id = ObjectId(com_id)
            com = self._com_worker.get_by_id(com_id)
        except InvalidId:
            return

        if com:
            if self._com_worker.edit_comment(com.id, cleaners.TextCleaner().clean(new_text)):
                return self._task_worker.get_by_id(com.task)

    def edit_task(self, task_id, title=None, description=None, task_type=None):
        task = self.get_task(task_id)

        if task:
            if title is None:
                title = task.title
            else:
                title = cleaners.TitleCleaner().clean(title)

            if description is None:
                description = task.description
            else:
                description = cleaners.TextCleaner().clean(description)

            if task_type is None:
                task_type = task.task_type

            if title == task.title and description == task.description and task_type == task.task_type:  # don't change
                return task

            return self._task_worker.edit_task(task.id, title, description, task_type)



    def has_action_rights(self, task, user, action: consts.TaskAction):
        """This method does not check task status, only roles"""
        pp = self._pp_worker.get_by_project_id_and_user_id(task.project, user.id)
        if pp:
            if pp.role == consts.RoleEnum.head:
                return True
            elif action == consts.TaskAction.finish:
                return task.executor == pp.id
            elif action in [consts.TaskAction.verify, consts.TaskAction.request_correction]:
                return task.checker == pp.id
            return action == consts.TaskAction.reopen
        return False

    def _set_executor(self, task, **kwargs):
        if task.status not in [consts.TaskStatus.new, consts.TaskStatus.reopened, consts.TaskStatus.open, consts.TaskStatus.correction]:
            return False
        if kwargs and 'pp_id' in kwargs.keys():
            try:
                ex_id = ObjectId(kwargs['pp_id'])
            except InvalidId:
                return False
            else:
                executor = self._pp_worker.get_by_id(ex_id)
                if not executor:
                    return False
                if task.executor != ex_id:
                    task = self._task_worker.set_executor(ex_id, task.id)
                    ts = self.subscribe_user_to_task(task.id, executor.user.id)
                    if ts:
                        task_url = urllib.parse.urljoin(config.SERVER_NAME, f"task/{str(task.id)}")
                        by_user = kwargs['__by_user__']
                        message = f'For task {task_url} @{executor.user.username} has been set as executor by user @{by_user.username}'
                        self._send_notification(message, self._ts_worker.get_by_task_id(task.id))
                if task:
                    return self._task_worker.set_status(consts.TaskStatus.open, task.id)

    def _set_tester(self, task, **kwargs):
        # TODO: send to test
        if task.status != consts.TaskStatus.ready:
            return False
        if kwargs and 'pp_id' in kwargs.keys():
            try:
                tester_id = ObjectId(kwargs['pp_id'])
            except InvalidId:
                return False
            else:
                tester = self._pp_worker.get_by_id(tester_id)
                if not tester:
                    return False
                if task.checker != tester_id:
                    task = self._task_worker.set_tester(tester_id, task.id)
                    ts = self.subscribe_user_to_task(task.id, tester.user.id)
                    if ts:
                        task_url = urllib.parse.urljoin(config.SERVER_NAME, f"task/{str(task.id)}")
                        by_user = kwargs['__by_user__']
                        message = f'For task {task_url} @{tester.user.username} has been set as tester by user @{by_user.username}'
                        self._send_notification(message, self._ts_worker.get_by_task_id(task.id))
                if task:
                    return self._task_worker.set_status(consts.TaskStatus.verification, task.id)

    def _reopen(self, task, **kwargs):
        if task.status != consts.TaskStatus.closed:
            return False
        by_user = kwargs['__by_user__']
        pp = self._pp_worker.get_by_project_id_and_user_id(task.project, by_user.id)
        if pp:
            task = self._task_worker.set_author(pp.id, task.id)
            return self._task_worker.set_status(consts.TaskStatus.reopened, task.id)

    def _verify(self, task, **kwargs):
        if task.status != consts.TaskStatus.verification:
            return False
        return self._task_worker.set_status(consts.TaskStatus.closed, task.id)

    def _request_correction(self, task, **kwargs):
        if task.status != consts.TaskStatus.verification:
            return False
        return self._task_worker.set_status(consts.TaskStatus.correction, task.id)

    def _finish(self, task, **kwargs):
        if task.status in [consts.TaskStatus.open, consts.TaskStatus.correction]:
            return False
        return self._task_worker.set_status(consts.TaskStatus.ready, task.id)

    def _close(self, task, **kwargs):
        return self._task_worker.set_status(consts.TaskStatus.closed, task.id)

    def _send_notification(self, message, subscribers):
        receivers = [subscriber.subscriber.user for subscriber in subscribers]
        send_message(message, receivers)

    def perform_action(self, task, user_id, action: consts.TaskAction, **kwargs):
        try:
            user_id = ObjectId(user_id)
            user = self._user_worker.get_by_id(user_id)
            if not self.has_action_rights(task, user, action):
                return False
        except InvalidId:
            return False

        kwargs['__by_user__'] = user
        old_status = task.status
        task = self._task_actions[action](task, **kwargs)
        if task and old_status != task.status:
            task_url = urllib.parse.urljoin(config.SERVER_NAME, f"task/{str(task.id)}")
            message = f'For task {task_url} has been changed status to {task.status.name} by user @{user.username}'
            self._send_notification(message, self._ts_worker.get_by_task_id(task.id))
        return task

    def notify_project_closing(self, task_id):
        task = self.get_task(task_id)
        if task:
            task_url = urllib.parse.urljoin(config.SERVER_NAME, f"task/{str(task.id)}")
            project_url = urllib.parse.urljoin(config.SERVER_NAME, f"project/{str(task.project)}")
            message = f'Project {project_url} is closing! Task {task_url} not closed yet.'
            self._send_notification(message, self._ts_worker.get_by_task_id(task.id))
