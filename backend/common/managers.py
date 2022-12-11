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
