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


class ProjectParticipantWorker(BaseDBWorker):
    def _factory(self, cursor):
        _user_worker = UserWorker()
        _project_worker = ProjectWorker()
        res = []
        users = []
        projects = []
        for pp in cursor:
            user = [_user for _user in users if pp['user'] != _user.id]
            if user:
                pp['user'] = user[0]
            else:
                pp['user'] = _user_worker.get_by_id(pp['user'])
                users.append(pp['user'])

            project = [_project for _project in projects if pp['project'] != _project.id]
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
