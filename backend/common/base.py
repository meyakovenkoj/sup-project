import typing

from bson.objectid import ObjectId
from datetime import datetime, date

from common import consts
from common.conf import config


class User:
    def __init__(
            self,
            id_obj: ObjectId,
            name: str,
            surname: str,
            username: str,
            password_hash: str,
            projects: typing.List["ProjectParticipant"],
            is_admin: bool
    ):
        self.user_id: ObjectId = id_obj
        self.name: str = name
        self.surname: str = surname
        self.username: str = username
        self.password_hash: str = password_hash
        self.projects: typing.List["ProjectParticipant"] = projects
        self.is_admin: bool = is_admin

    def __iter__(self):
        yield "id", str(self.user_id)
        yield "name", self.name
        yield "surname", self.surname
        yield "username", self.username
        yield "projects", [dict(project) for project in self.projects]
        yield "is_admin", self.is_admin


class Project:
    def __init__(
            self,
            id_obj: ObjectId,
            title: str,
            head: typing.Optional["ProjectParticipant"],
            created: date,
            participants: typing.List["ProjectParticipant"],
            tasks: typing.List["Task"],
            status: consts.ProjectStatus
    ):
        self.project_id: ObjectId = id_obj
        self.title: str = title
        self.head: typing.Optional["ProjectParticipant"] = head
        self.created: date = created
        self.participants: typing.List["ProjectParticipant"] = participants
        self.tasks: typing.List["Task"] = tasks
        self.status: consts.ProjectStatus = status

    def __iter__(self):
        yield "id", str(self.project_id)
        yield "title", self.title
        yield "head", dict(self.head) if self.head is not None else None
        yield "created", self.created.strftime(config.DATE_FMT)
        yield "participants", [dict(participant) for participant in self.participants]
        yield "tasks", [dict(task) for task in self.tasks]
        yield "status", self.status.name


class ProjectParticipant:
    def __init__(
            self,
            id_obj: ObjectId,
            role: consts.RoleEnum,
            user: User,
            project: Project,
            subscriptions: typing.List["TaskSubscriber"]
    ):
        self.pp_id: ObjectId = id_obj
        self.role: consts.RoleEnum = role
        self.user: User = user
        self.project: Project = project
        self.subscriptions: typing.List["TaskSubscriber"] = subscriptions

    def __iter__(self):
        yield "id", str(self.pp_id)
        yield "role", self.role.name
        yield "user", dict(self.user)
        yield "project", dict(self.project)
        yield "subscriptions", [dict(subscription) for subscription in self.subscriptions]


class Task:
    def __init__(
            self,
            id_obj: ObjectId,
            title: str,
            author: ProjectParticipant,
            created: datetime,
            changed: typing.Optional[datetime],
            executor: typing.Optional[ProjectParticipant],
            accepted: typing.Optional[datetime],
            description: str,
            checker: typing.Optional[ProjectParticipant],
            status: consts.TaskStatus,
            subscribers: typing.List["TaskSubscriber"],
            project: Project,
            comments: typing.List["Comment"],
            files: typing.List[str],
            task_type: consts.TaskType
    ):
        self.task_id: ObjectId = id_obj
        self.title: str = title
        self.author: ProjectParticipant = author
        self.created: datetime = created
        self.changed: typing.Optional[datetime] = changed
        self.executor: typing.Optional[ProjectParticipant] = executor
        self.accepted: typing.Optional[datetime] = accepted
        self.description: str = description
        self.checker: typing.Optional[ProjectParticipant] = checker
        self.status: consts.TaskStatus = status
        self.subscribers: typing.List["TaskSubscriber"] = subscribers
        self.project: Project = project
        self.comments: typing.List["Comment"] = comments
        self.files: typing.List[str] = files
        self.task_type: consts.TaskType = task_type

    def __iter__(self):
        yield "id", str(self.task_id)
        yield "title", self.title
        yield "author", dict(self.author)
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


class TaskSubscriber:
    def __init__(
            self,
            id_obj: ObjectId,
            task: Task,
            subscriber: ProjectParticipant
    ):
        self.ts_id: ObjectId = id_obj
        self.task: Task = task
        self.subscriber: ProjectParticipant = subscriber

    def __iter__(self):
        yield "id", str(self.ts_id)
        yield "task", dict(self.task)
        yield "subscriber", dict(self.subscriber)


class Comment:
    def __init__(
            self,
            id_obj: ObjectId,
            text: str,
            author: User,
            created: datetime,
            edited: typing.Optional[datetime]
    ):
        self.comment_id: ObjectId = id_obj
        self.text: str = text
        self.author: User = author
        self.created: datetime = created
        self.edited: typing.Optional[datetime] = edited

    def __iter__(self):
        yield "id", str(self.comment_id)
        yield "text", self.text
        yield "author", dict(self.author)
        yield "created", self.created.strftime(config.DATETIME_FMT)
        yield "edited", self.edited.strftime(config.DATETIME_FMT) if self.edited is not None else None
