import typing
import re

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from pymongo.collection import Collection
from bson.errors import InvalidId
from datetime import date, datetime

from common import managers, base, consts
from common.logger import get_logger
from common.conf import config


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db

    return db


# SESSION WORKERS


class UserLogin:
    def __init__(self, user: base.User):
        self.__user = user

    def get_id(self):
        return str(self.__user.id)

    def is_authenticated(self):
        return True if self.__user else False

    def is_anonymous(self):
        return False if self.__user else True

    def is_active(self):
        return True if self.__user else False

    def get_name(self):
        return self.__user.username if self.__user else None

    def is_admin(self):
        return self.__user.is_admin if self.__user else None


# DATABASE WORKERS


class BaseDBWorker:
    db = LocalProxy(get_db)  # Use LocalProxy to read the global db instance with just `db`

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def _factory(self, cursor):
        raise NotImplementedError(f"_factory method of {self.__class__.__name__} must be implemented!")

    def select(self, callback: callable, *args):
        return self._factory(callback(*args))

    def insert(self, collection: Collection, *args):
        res = collection.insert_one(*args)
        self.logger.info(f"Insert result: id={res.inserted_id}, ack={res.acknowledged}")
        return res

    def update(self, collection: Collection, *args):
        res = collection.update_one(*args)
        self.logger.info(f"Update result: {res.raw_result}, matched={res.matched_count}, modified={res.modified_count}, ack={res.acknowledged}")
        return res

    def delete(self, collection: Collection, *args, one=True):
        if one:
            res = collection.delete_one(*args)
        else:
            res = collection.delete_many(*args)
        self.logger.info(f"Delete result: {res.raw_result}, deleted={res.deleted_count}, ack={res.acknowledged}")
        return res


class UserWorker(BaseDBWorker):
    def _factory(self, cursor):
        return [managers.UserManager.from_db_dict(user) for user in cursor]

    def get_by_username(self, username: str) -> typing.Optional[base.User]:
        self.logger.info('Collecting users by username')
        res = self.select(self.db.User.find, {"username": username})
        return res[0] if res else None

    def get_by_id(self, user_id: ObjectId) -> typing.Optional[base.User]:
        self.logger.info('Collecting users by id')
        res = self.select(self.db.User.find, {"_id": user_id})
        return res[0] if res else None

    def create_user(self, username, password_hash, name, surname) -> typing.Optional[base.User]:
        self.logger.info('Creating new user')
        res = self.insert(self.db.User, {
            "name": name,
            "surname": surname,
            "username": username,
            "password_hash": password_hash,
            "projects": [],
            "is_admin": False
        })
        if res.inserted_id is not None:
            return self.get_by_id(res.inserted_id)

    def get_by_username_like(self, username_match: str) -> typing.List[base.User]:
        self.logger.info('Collecting users by username match')
        rgx = re.compile(f'.*{username_match}.*', re.IGNORECASE)
        res = self.select(self.db.User.find, {"username": rgx})
        return res

    def add_project(self, user_id: ObjectId, pp_id: ObjectId) -> typing.Optional[base.User]:
        user = self.get_by_id(user_id)
        if user:
            self.logger.info(f'adding participant to user')
            if pp_id not in user.projects:
                user.projects.append(pp_id)
            set_dict = {
                "projects": user.projects
            }
            res = self.update(self.db.User, {'_id': user_id}, {"$set": set_dict})
            if res.modified_count > 0:
                return self.get_by_id(user_id)


class ProjectWorker(BaseDBWorker):
    def _factory(self, cursor):
        return [managers.ProjectManager.from_db_dict(proj) for proj in cursor]

    def get_by_id(self, project_id: ObjectId) -> typing.Optional[base.Project]:
        self.logger.info('Collecting projects by id')
        res = self.select(self.db.Project.find, {"_id": project_id})
        return res[0] if res else None

    def get_by_title(self, title: str) -> typing.Optional[base.Project]:
        self.logger.info('Collecting projects by title')
        res = self.select(self.db.Project.find, {"title": title})
        return res[0] if res else None

    def get_by_title_like(self, title_match: str) -> typing.List[base.Project]:
        self.logger.info('Collecting projects by title match')
        rgx = re.compile(f'.*{title_match}.*', re.IGNORECASE)
        res = self.select(self.db.Project.find, {"title": rgx})
        return res

    def add_project(self, title: str) -> typing.Optional[base.Project]:
        self.logger.info('Creating new project')
        res = self.insert(self.db.Project, {
            "title": title,
            "created": datetime.now().date().strftime(config.DATE_FMT),
            "participants": [],
            "tasks": [],
            "status": consts.ProjectStatus.open.value,
        })
        if res.inserted_id is not None:
            return self.get_by_id(res.inserted_id)

    def set_head(self, head: ObjectId, project_id: ObjectId) -> typing.Optional[base.Project]:
        self.logger.info(f'Setting project head')
        res = self.update(self.db.Project, {'_id': project_id}, {"$set": {'head': head}})
        if res.modified_count > 0:
            return self.get_by_id(project_id)

    def add_participant(self, project_id: ObjectId, pp_id: ObjectId, as_head: bool = False) -> typing.Optional[base.Project]:
        project = self.get_by_id(project_id)
        if project:
            self.logger.info(f'adding participant to the project')
            if pp_id not in project.participants:
                project.participants.append(pp_id)
            set_dict = {
                "participants": project.participants
            }
            if as_head:
                set_dict['head'] = pp_id
            res = self.update(self.db.Project, {'_id': project_id}, {"$set": set_dict})
            if res.modified_count > 0:
                return self.get_by_id(project_id)

    def set_status(self, status: consts.ProjectStatus, project_id: ObjectId) -> typing.Optional[base.Project]:
        self.logger.info(f'Setting project status')
        res = self.update(self.db.Project, {'_id': project_id}, {"$set": {'status': status.value}})
        if res.modified_count > 0:
            return self.get_by_id(project_id)

    def add_task(self, project_id: ObjectId, task_id: ObjectId) -> typing.Optional[base.Project]:
        self.logger.info(f'Adding task to project')
        res = self.update(self.db.Project, {'_id': project_id}, {"$addToSet": {'tasks': task_id}})
        if res.modified_count > 0:
            return self.get_by_id(project_id)


class ProjectParticipantWorker(BaseDBWorker):
    def _factory(self, cursor):
        _user_worker = UserWorker()
        _project_worker = ProjectWorker()
        res = []
        users = []
        projects = []
        for pp in cursor:
            user = [_user for _user in users if pp['user'] == _user.id]
            if user:
                pp['user'] = user[0]
            else:
                pp['user'] = _user_worker.get_by_id(pp['user'])
                users.append(pp['user'])

            project = [_project for _project in projects if pp['project'] == _project.id]
            if project:
                pp['project'] = project[0]
            else:
                pp['project'] = _project_worker.get_by_id(pp['project'])
                projects.append(pp['project'])
            res.append(managers.ProjectParticipantManager.from_db_dict(pp))

        return res

    def get_by_id(self, pp_id: ObjectId) -> typing.Optional[base.ProjectParticipant]:
        self.logger.info('Collecting projects participants by id')
        res = self.select(self.db.ProjectParticipant.find, {"_id": pp_id})
        return res[0] if res else None

    def get_by_project_id(self, project_id: ObjectId) -> typing.List[base.ProjectParticipant]:
        self.logger.info('Collecting projects participants by project id')
        res = self.select(self.db.ProjectParticipant.find, {"project": project_id})
        return res

    def get_by_user_id(self, user_id: ObjectId) -> typing.List[base.ProjectParticipant]:
        self.logger.info('Collecting projects participants by user id')
        res = self.select(self.db.ProjectParticipant.find, {"user": user_id})
        return res

    def get_by_project_id_and_user_id(self, project_id: ObjectId, user_id: ObjectId) -> typing.Optional[base.ProjectParticipant]:
        self.logger.info('Collecting projects participants by project id and user id')
        res = self.select(self.db.ProjectParticipant.find, {"project": project_id, "user": user_id})
        return res[0] if res else None

    def create_pp(
            self,
            user_id: ObjectId,
            project_id: ObjectId,
            role: consts.RoleEnum = consts.RoleEnum.worker
    ) -> typing.Optional[base.ProjectParticipant]:
        self.logger.info('Creating new project participant')
        res = self.insert(self.db.ProjectParticipant, {
            "role": role.value,
            "user": user_id,
            "project": project_id,
            "subscriptions": []
        })
        if res.inserted_id is not None:
            return self.get_by_id(res.inserted_id)

    def update_role(self, pp_id: ObjectId, role: consts.RoleEnum) -> typing.Optional[base.ProjectParticipant]:
        self.logger.info(f'Updating project participant role')
        res = self.update(self.db.ProjectParticipant, {'_id': pp_id}, {"$set": {'role': role.value}})
        if res.modified_count > 0:
            return self.get_by_id(pp_id)

    def add_subscription(self, pp_id: ObjectId, ts_id: ObjectId) -> typing.Optional[base.ProjectParticipant]:
        self.logger.info(f'Updating project participant subscriptions')
        res = self.update(self.db.ProjectParticipant, {'_id': pp_id}, {"$addToSet": {'subscriptions': ts_id}})
        if res.modified_count > 0:
            return self.get_by_id(pp_id)

    def remove_subscription(self, pp_id: ObjectId, ts_id: ObjectId) -> typing.Optional[base.ProjectParticipant]:
        self.logger.info(f'Updating project participant subscriptions')
        res = self.update(self.db.ProjectParticipant, {'_id': pp_id}, {"$pull": {'subscriptions': ts_id}})
        if res.modified_count > 0:
            return self.get_by_id(pp_id)


class TaskWorker(BaseDBWorker):
    def _factory(self, cursor):
        return [managers.TaskManager.from_db_dict(task) for task in cursor]

    def get_by_id(self, task_id: ObjectId) -> typing.Optional[base.Task]:
        self.logger.info('Collecting tasks by id')
        res = self.select(self.db.Task.find, {"_id": task_id})
        return res[0] if res else None

    def get_by_title(self, title: str) -> typing.Optional[base.Project]:
        self.logger.info('Collecting tasks by title')
        res = self.select(self.db.Task.find, {"title": title})
        return res

    def get_by_title_like(self, title_match: str) -> typing.List[base.Task]:
        self.logger.info('Collecting tasks by title match')
        rgx = re.compile(f'.*{title_match}.*', re.IGNORECASE)
        res = self.select(self.db.Task.find, {"title": rgx})
        return res

    def get_by_pp_assigned(self, pp_id: ObjectId) -> typing.List[base.Task]:
        self.logger.info('Collecting tasks by project participant')
        query = '''function() {'''\
            f'''
               return (this.executor == "{pp_id}" || this.tester == "{pp_id}")
            '''\
            '''}'''
        res = self.select(self.db.Task.find, {"$where": query})
        return res

    def add_task(self, title: str, description: str, author_id: ObjectId, project_id: ObjectId, task_type: consts.TaskType) -> typing.Optional[base.Task]:
        self.logger.info('Creating new task')
        res = self.insert(self.db.Task, {
            "title": title,
            "author": author_id,
            "created": datetime.now().strftime(config.DATETIME_FMT),
            "description": description,
            "status": consts.TaskStatus.new.value,
            "subscribers": [],
            "project": project_id,
            "comments": [],
            "files": [],
            "task_type": task_type.value
        })
        if res.inserted_id is not None:
            return self.get_by_id(res.inserted_id)

    def update_attachments(self, task_id: ObjectId, files: typing.List[str]) -> typing.Optional[base.Task]:
        self.logger.info(f'Updating task attachments')
        res = self.update(self.db.Task, {'_id': task_id}, {"$set": {'files': files, "changed": datetime.now().strftime(config.DATETIME_FMT)}})
        if res.modified_count > 0:
            return self.get_by_id(task_id)

    def add_subscriber(self, task_id: ObjectId, ts_id: ObjectId) -> typing.Optional[base.Task]:
        self.logger.info(f'Updating task subscribers')
        res = self.update(self.db.Task, {'_id': task_id}, {"$addToSet": {'subscribers': ts_id}})
        if res.modified_count > 0:
            return self.get_by_id(task_id)

    def remove_subscriber(self, task_id: ObjectId, ts_id: ObjectId) -> typing.Optional[base.Task]:
        self.logger.info(f'Updating task subscribers')
        res = self.update(self.db.Task, {'_id': task_id}, {"$pull": {'subscribers': ts_id}})
        if res.modified_count > 0:
            return self.get_by_id(task_id)

    def set_status(self, status: consts.TaskStatus, task_id: ObjectId) -> typing.Optional[base.Task]:
        self.logger.info(f'Setting task status')
        res = self.update(self.db.Task, {'_id': task_id}, {"$set": {'status': status.value, "changed": datetime.now().strftime(config.DATETIME_FMT)}})
        if res.modified_count > 0:
            return self.get_by_id(task_id)

    def set_executor(self, pp_id: ObjectId, task_id: ObjectId) -> typing.Optional[base.Task]:
        self.logger.info(f'Setting task executor')
        res = self.update(self.db.Task, {'_id': task_id}, {"$set": {'executor': pp_id, "changed": datetime.now().strftime(config.DATETIME_FMT)}})
        if res.modified_count > 0:
            return self.get_by_id(task_id)

    def set_tester(self, pp_id: ObjectId, task_id: ObjectId) -> typing.Optional[base.Task]:
        self.logger.info(f'Setting task checker')
        res = self.update(self.db.Task, {'_id': task_id}, {"$set": {'checker': pp_id, "changed": datetime.now().strftime(config.DATETIME_FMT)}})
        if res.modified_count > 0:
            return self.get_by_id(task_id)

    def set_author(self, pp_id: ObjectId, task_id: ObjectId) -> typing.Optional[base.Task]:
        self.logger.info(f'Setting task author')
        res = self.update(self.db.Task, {'_id': task_id}, {"$set": {'author': pp_id, "changed": datetime.now().strftime(config.DATETIME_FMT)}})
        if res.modified_count > 0:
            return self.get_by_id(task_id)


class TaskSubscriberWorker(BaseDBWorker):
    def _factory(self, cursor):
        _task_worker = TaskWorker()
        _pp_worker = ProjectParticipantWorker()
        res = []
        tasks = []
        pps = []
        for ts in cursor:
            task = [_task for _task in tasks if ts['task'] == _task.id]
            if task:
                ts['task'] = task[0]
            else:
                ts['task'] = _task_worker.get_by_id(ts['task'])
                tasks.append(ts['task'])

            pp = [_pp for _pp in pps if ts['subscriber'] == _pp.id]
            if pp:
                ts['subscriber'] = pp[0]
            else:
                ts['subscriber'] = _pp_worker.get_by_id(ts['subscriber'])
                pps.append(ts['subscriber'])

            res.append(managers.TaskSubscriberManager.from_db_dict(ts))

        return res

    def get_by_id(self, ts_id: ObjectId) -> typing.Optional[base.TaskSubscriber]:
        self.logger.info('Collecting tasks subscribers by id')
        res = self.select(self.db.TaskSubscriber.find, {"_id": ts_id})
        return res[0] if res else None

    def get_by_project_participant_id(self, pp_id: ObjectId) -> typing.List[base.TaskSubscriber]:
        self.logger.info('Collecting tasks subscribers by project participant id')
        res = self.select(self.db.TaskSubscriber.find, {"subscriber": pp_id})
        return res

    def get_by_task_id(self, task_id: ObjectId) -> typing.List[base.TaskSubscriber]:
        self.logger.info('Collecting tasks subscribers by task id')
        res = self.select(self.db.TaskSubscriber.find, {"task": task_id})
        return res

    def get_by_task_id_and_project_participant_id(
            self, pp_id: ObjectId, task_id: ObjectId
    ) -> typing.Optional[base.TaskSubscriber]:
        self.logger.info('Collecting tasks subscribers by task_id and pp_id')
        res = self.select(self.db.TaskSubscriber.find, {"task": task_id, "subscriber": pp_id})
        return res[0] if res else None

    def create_ts(
            self,
            task_id: ObjectId,
            pp_id: ObjectId
    ) -> typing.Optional[base.TaskSubscriber]:
        self.logger.info('Creating new task subscriber')
        res = self.insert(self.db.TaskSubscriber, {
            "task": task_id,
            "subscriber": pp_id
        })
        if res.inserted_id is not None:
            return self.get_by_id(res.inserted_id)

    def remove_ts(self, ts_is: ObjectId) -> bool:
        self.logger.info("Removing subscription")
        res = self.delete(self.db.TaskSubscriber, {
            "_id": ts_is
        }, one=True)
        return res.deleted_count > 0
