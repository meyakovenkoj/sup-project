

from common.base import User


class UserManager:
    @staticmethod
    def from_db_dict(data):
        return User(
            id_obj=data['_id'],
            name=data['name'],
            surname=data['surname'],
            username=data['username'],
            password_hash=data['password_hash'],
            projects=data['projects'],
            is_admin=data['is_admin']
        )
