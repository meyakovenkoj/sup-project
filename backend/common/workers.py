import typing

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from pymongo.collection import Collection
from bson.errors import InvalidId

from common import managers, base
from common.logger import get_logger


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
        return str(self.__user.user_id)

    def is_authenticated(self):
        return True if self.__user else False

    def is_anonymous(self):
        return False if self.__user else True

    def is_active(self):
        return True if self.__user else False

    def get_name(self):
        return self.__user.username if self.__user else None


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
            "is_admin": True
        })
        if res.inserted_id is not None:
            return self.get_by_id(res.inserted_id)


