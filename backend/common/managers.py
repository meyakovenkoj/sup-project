from datetime import date, datetime

from common.conf import config
from common import base, consts


class UserManager:
    @staticmethod
    def from_db_dict(data):
        return base.User(
            id_obj=data['_id'],
            name=data['name'],
            surname=data['surname'],
            username=data['username'],
            password_hash=data['password_hash'],
            projects=data['projects'],
            is_admin=data['is_admin']
        )


class ProjectManager:
    @staticmethod
    def from_db_dict(data):
        head = data.get('head')
        if isinstance(head, dict):
            head = UserManager.from_db_dict(head)

        status = data['status']
        if isinstance(status, str):
            status = consts.ProjectStatus[status]
        elif isinstance(status, int):
            status = consts.ProjectStatus(status)

        return base.Project(
            id_obj=data['_id'],
            title=data['title'],
            head=head,
            created=datetime.strptime(data['created'], config.DATE_FMT).date(),
            participants=data['participants'],
            tasks=data['tasks'],
            status=status
        )


class ProjectParticipantManager:
    @staticmethod
    def from_db_dict(data):
        pp = base.ProjectParticipant(
            id_obj=data['_id'],
            role=consts.RoleEnum[data['role']] if isinstance(data['role'], str) else consts.RoleEnum(data['role']),
            user=data['user'],
            project=data['project'],
            subscriptions=data['subscriptions']
        )
        if pp.id in pp.project.participants:
            pp.project.participants.remove(pp.id)
        pp.project.participants.append(pp)
        if pp.project.head and pp.project.head == pp.id:
            pp.project.head = pp
        if pp.id in pp.user.projects:
            pp.user.projects.remove(pp.id)
        pp.user.projects.append(pp)
        return pp


class TaskManager:
    @staticmethod
    def from_db_dict(data):
        author = data.get('author')
        if isinstance(author, dict):
            author = UserManager.from_db_dict(author)

        executor = data.get('executor')
        if isinstance(executor, dict):
            executor = UserManager.from_db_dict(executor)

        checker = data.get('checker')
        if isinstance(checker, dict):
            checker = UserManager.from_db_dict(checker)

        status = data['status']
        if isinstance(status, str):
            status = consts.TaskStatus[status]
        elif isinstance(status, int):
            status = consts.TaskStatus(status)

        task_type = data['task_type']
        if isinstance(task_type, str):
            task_type = consts.TaskType[task_type]
        elif isinstance(task_type, int):
            task_type = consts.TaskType(task_type)

        changed = data.get('changed')
        if changed:
            changed = datetime.strptime(changed, config.DATE_FMT)

        accepted = data.get('accepted')
        if accepted:
            accepted = datetime.strptime(accepted, config.DATE_FMT)

        return base.Task(
            id_obj=data['_id'],
            title=data['title'],
            author=author,
            created=datetime.strptime(data['created'], config.DATE_FMT),
            status=status,
            task_type=task_type,
            executor=executor,
            checker=checker,
            changed=changed,
            accepted=accepted,
            files=data['files'],
            comments=data['comments'],
            project=data['project'],
            description=data['description'],
            subscribers=data['subscribers']
        )
