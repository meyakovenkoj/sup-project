import string

from enum import IntEnum


class RoleEnum(IntEnum):
    head = 1
    worker = 2


class ProjectStatus(IntEnum):
    open = 1
    closed = 2
    archived = 3


class TaskType(IntEnum):
    bug = 1
    task = 2
    feature = 3
    story = 4


class TaskStatus(IntEnum):
    new = 1
    open = 2
    reopened = 3
    ready = 4
    verification = 5
    closed = 6
    correction = 7


MIN_PASSWORD_LEN = 12
PASSWORD_SIMBOLS = string.ascii_letters + string.digits + string.punctuation
USERNAME_SIMBOLS = string.ascii_letters + string.digits


class ProjectAction(IntEnum):
    close = 1
    archive = 2
    reopen = 3
