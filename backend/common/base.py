import typing

from bson.objectid import ObjectId
from datetime import datetime, date

from common import consts
from common.conf import config


class BaseClass:
    def __init__(self, id_obj: ObjectId):
        self._id = id_obj

    @property
    def id(self):
        return self._id

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id == other._id
        return False


class User(BaseClass):
    def __init__(
            self,
            id_obj: ObjectId,
            name: str,
            surname: str,
            username: str,
            password_hash: str,
            projects: typing.List[typing.Union["ProjectParticipant", ObjectId]],
            is_admin: bool
    ):
        super().__init__(id_obj)
        self.name: str = name
        self.surname: str = surname
        self.username: str = username
        self.password_hash: str = password_hash
        self.projects: typing.List[typing.Union["ProjectParticipant", ObjectId]] = projects
        self.is_admin: bool = is_admin

    def __iter__(self):
        yield "id", str(self._id)
        yield "name", self.name
        yield "surname", self.surname
        yield "username", self.username
        yield "projects", [project for project in self.projects]
        yield "is_admin", self.is_admin


class Project(BaseClass):
    def __init__(
            self,
            id_obj: ObjectId,
            title: str,
            head: typing.Optional[typing.Union["ProjectParticipant", ObjectId]],
            created: date,
            participants: typing.List[typing.Union["ProjectParticipant", ObjectId]],
            tasks: typing.List[typing.Union["Task", ObjectId]],
            status: consts.ProjectStatus
    ):
        super().__init__(id_obj)
        self.title: str = title
        self.head: typing.Optional[typing.Union["ProjectParticipant", ObjectId]] = head
        self.created: date = created
        self.participants: typing.List[typing.Union["ProjectParticipant", ObjectId]] = participants
        self.tasks: typing.List[typing.Union["Task", ObjectId]] = tasks
        self.status: consts.ProjectStatus = status

    def __iter__(self):
        yield "id", str(self._id)
        yield "title", self.title
        yield "head", self.head
        yield "created", self.created.strftime(config.DATE_FMT)
        yield "participants", [participant for participant in self.participants]
        yield "tasks", [task for task in self.tasks]
        yield "status", self.status.name


class ProjectParticipant(BaseClass):
    def __init__(
            self,
            id_obj: ObjectId,
            role: consts.RoleEnum,
            user: User,
            project: Project,
            subscriptions: typing.List[typing.Union["TaskSubscriber", ObjectId]]
    ):
        super().__init__(id_obj)
        self.role: consts.RoleEnum = role
        self.user: User = user
        self.project: Project = project
        self.subscriptions: typing.List[typing.Union["TaskSubscriber", ObjectId]] = subscriptions

    def __iter__(self):
        yield "id", str(self._id)
        yield "role", self.role.name
        yield "user", self.user
        yield "project", self.project
        yield "subscriptions", [subscription for subscription in self.subscriptions]


class Task(BaseClass):
    def __init__(
            self,
            id_obj: ObjectId,
            title: str,
            author: typing.Union[ProjectParticipant, ObjectId],
            created: datetime,
            changed: typing.Optional[datetime],
            executor: typing.Optional[typing.Union[ProjectParticipant, ObjectId]],
            accepted: typing.Optional[datetime],
            description: str,
            checker: typing.Optional[typing.Union[ProjectParticipant, ObjectId]],
            status: consts.TaskStatus,
            subscribers: typing.List[typing.Union["TaskSubscriber", ObjectId]],
            project: Project,
            comments: typing.List[typing.Union["Comment", ObjectId]],
            files: typing.List[str],
            task_type: consts.TaskType
    ):
        super().__init__(id_obj)
        self.title: str = title
        self.author: typing.Union[ProjectParticipant, ObjectId] = author
        self.created: datetime = created
        self.changed: typing.Optional[datetime] = changed
        self.executor: typing.Optional[typing.Union[ProjectParticipant, ObjectId]] = executor
        self.accepted: typing.Optional[datetime] = accepted
        self.description: str = description
        self.checker: typing.Optional[typing.Union[ProjectParticipant, ObjectId]] = checker
        self.status: consts.TaskStatus = status
        self.subscribers: typing.List[typing.Union["TaskSubscriber", ObjectId]] = subscribers
        self.project: Project = project
        self.comments: typing.List[typing.Union["Comment", ObjectId]] = comments
        self.files: typing.List[str] = files
        self.task_type: consts.TaskType = task_type

    def __iter__(self):
        yield "id", str(self._id)
        yield "title", self.title
        yield "author", self.author
        yield "created", self.created.strftime(config.DATETIME_FMT)
        yield "changed", self.changed.strftime(config.DATETIME_FMT) if self.changed is not None else None
        yield "executor", self.executor
        yield "accepted", self.accepted.strftime(config.DATETIME_FMT) if self.accepted is not None else None
        yield "description", self.description
        yield "checker", self.checker
        yield "status", self.status
        yield "subscribers", self.subscribers
        yield "project", self.project
        yield "comments", self.comments
        yield "files", self.files
        yield "task_type", self.task_type


class TaskSubscriber(BaseClass):
    def __init__(
            self,
            id_obj: ObjectId,
            task: Task,
            subscriber: ProjectParticipant
    ):
        super().__init__(id_obj)
        self.task: Task = task
        self.subscriber: ProjectParticipant = subscriber

    def __iter__(self):
        yield "id", str(self._id)
        yield "task", self.task
        yield "subscriber", self.subscriber


class Comment(BaseClass):
    def __init__(
            self,
            id_obj: ObjectId,
            text: str,
            author: User,
            task: Task,
            created: datetime,
            edited: typing.Optional[datetime]
    ):
        super().__init__(id_obj)
        self.text: str = text
        self.author: User = author
        self.task: Task = task  # TODO add to classes and schema
        self.created: datetime = created
        self.edited: typing.Optional[datetime] = edited

    def __iter__(self):
        yield "id", str(self._id)
        yield "text", self.text
        yield "author", self.author
        yield "task", self.task
        yield "created", self.created.strftime(config.DATETIME_FMT)
        yield "edited", self.edited.strftime(config.DATETIME_FMT) if self.edited is not None else None
