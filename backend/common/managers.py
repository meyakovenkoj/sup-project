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
        proj = ProjectManager.from_db_dict(data['project'])
        user = UserManager.from_db_dict(data['user'])
        pp = base.ProjectParticipant(
            id_obj=data['_id'],
            role=consts.RoleEnum[data['role']],
            user=user,
            project=proj,
            subscriptions=data['subscriptions']
        )
        proj.participants.remove(pp.pp_id)
        proj.participants.append(pp)
        if proj.head and proj.head == pp.pp_id:
            proj.head = pp
        user.projects.remove(pp.pp_id)
        user.projects.append(pp)
        return pp
