from flask import Blueprint, request
from flask_login import login_required

from common import controllers, consts
from common.logger import get_logger
from common.json_response import json_response

logger = get_logger(name="user-views")
user_view = Blueprint("user_view", __name__)


@user_view.route('/_xhr/users', methods=['GET'])
@login_required
def user_by_username():
    username = request.args.get('username')
    username_match = request.args.get('username_match')
    if username:
        user = controllers.UserController().get_user_by_username(username)
        return json_response(data={
            "data": {
                "user": user
            }
        }, status_code=200 if user else 404)
    elif username_match:
        users_list = controllers.UserController().find_user_by_username(username_match)
        return json_response(data={
            "data": {
                "users": users_list
            }
        }, status_code=200 if users_list else 404)
    else:
        return json_response({'message': 'Bad request'}, 400)


@user_view.route('/_xhr/users/<string:user_id>', methods=['GET'])
@login_required
def user_by_id(user_id):
    if user_id:
        user = controllers.UserController().get_user(user_id)
        return json_response(data={
            "data": {
                "user": user
            }
        }, status_code=200 if user else 404)
    else:
        return json_response({'message': 'Bad request'}, 400)
