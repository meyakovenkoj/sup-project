import os
import secrets

import simplejson as json
from pathlib import Path
from flask import Flask, Response, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from common.conf import config
from common.logger import get_logger
from common import workers, controllers

logger = get_logger(name='main-server')
app = Flask(__name__, static_url_path='/static', template_folder='/template')

app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

app.config["MONGO_URI"] = config.MONGO_URI
mongo = PyMongo(app)

SECRET_FILE_PATH = Path(config.SECRET_KEY_FILENAME)
try:
    with SECRET_FILE_PATH.open("r") as secret_file:
        app.secret_key = secret_file.read()
except FileNotFoundError:
    # Let's create a cryptographically secure code in that file
    with SECRET_FILE_PATH.open("w") as secret_file:
        app.secret_key = secrets.token_hex(32)
        secret_file.write(app.secret_key)


login_manager = LoginManager()
login_manager.init_app(app)


def my_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return dict(obj)


def _json_response(data, status_code=200):
    try:
        return Response(response=json.dumps(data, default=my_serializer), status=status_code,
                        mimetype='application/json')
    except Exception as e:
        logger.exception(f'Json serialize error: {e}')
        abort(400, 'Invalid json')


@login_manager.user_loader
def load_user(user_id):
    return controllers.AuthorizationController().get_user(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return _json_response({'message': 'Login required'}, 401)


@app.route('/_xhr/login', methods=['POST'])
def login():
    credentials = request.get_json()
    if credentials and 'username' in credentials.keys() and 'password' in credentials.keys():
        user = controllers.AuthorizationController().login_user(credentials['username'], credentials['password'])
        if user:
            login_user(user)
            logger.info(f'Successful login for user: {user.get_name()}')
            return _json_response({'message': 'Successful login'}, 200)
        else:
            logger.info('Failed authorization')
            return _json_response({'message': 'Wrong credentials'}, 401)
    else:
        return _json_response({'message': 'Bad request'}, 400)


@app.route('/_xhr/register', methods=['POST'])
def register():
    credentials = request.get_json()
    if credentials and 'username' in credentials.keys() and 'password' in credentials.keys() and 'name' in credentials.keys() and 'surname' in credentials.keys():
        _auth_controller = controllers.AuthorizationController()
        username, password, name, surname = credentials['username'], credentials['password'], credentials['name'], credentials['surname']
        if not _auth_controller.check_username_free(username):
            logger.info('Username already in use')
            return _json_response({'message': 'Username already in use'}, 400)
        if not _auth_controller.validate_creds(username, password, name, surname):
            logger.info('Failed creds validation')
            return _json_response({'message': 'Failed creds validation'}, 400)
        user = _auth_controller.register(username, password, name, surname)
        if user:
            login_user(user)
            logger.info(f'Successful register and login for user: {user.get_name()}')
            return _json_response({'message': 'Successful register'}, 201)
        else:
            logger.info('Failed register')
            return _json_response({'message': 'Wrong credentials'}, 401)
    else:
        return _json_response({'message': 'Bad request'}, 400)


@app.route('/_xhr/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return _json_response({'message': 'Successful logout'}, 200)


def __project_from_participant(pp):
    project = pp.project
    pp.project = project.id
    if pp in pp.user.projects:
        pp.user.projects.remove(pp)
        pp.user.projects.append(pp.id)
    return project


@app.route('/_xhr/project', methods=['POST'])
@login_required
def new_project():
    if not current_user.is_admin():
        return _json_response({'message': "You do not have admin rights"}, 405)
    data = request.get_json()
    if data and 'title' in data.keys():
        title = data['title']
        project_controller = controllers.ProjectController()
        if not project_controller.validate_title(title):
            logger.info('Failed title validation')
            return _json_response({'message': 'Failed title validation'}, 400)
        if not project_controller.check_title_free(title):
            logger.info('Title already in use')
            return _json_response({'message': 'Title already in use'}, 400)
        project = project_controller.create_project(title)
        if project:
            logger.info('Project created')
            return _json_response(
                {
                    'message': 'Project created',
                    'data': {'project': project}
                }, 201)
        else:
            logger.info('Failed project creation')
            return _json_response({'message': 'Project not created'}, 400)
    else:
        return _json_response({'message': 'Bad request'}, 400)


@app.route('/_xhr/project/head', methods=['POST'])
@login_required
def set_project_head():
    if not current_user.is_admin():
        return _json_response({'message': "You do not have admin rights"}, 405)
    data = request.get_json()
    if data and 'user_id' in data.keys() and 'project_id' in data.keys():
        user_id = data['user_id']
        if not controllers.UserController().get_user(user_id):
            logger.info('No such user')
            return _json_response({'message': 'No such user'}, 400)
        project_id = data['project_id']
        project_controller = controllers.ProjectController()
        pp = project_controller.set_head(project_id, user_id)
        if not pp:
            logger.info('No such project')
            return _json_response({'message': 'No such project'}, 400)

        project = __project_from_participant(pp)
        logger.info('Project head updated')
        return _json_response(
            {
                'message': 'Project head updated',
                'data': {'project': project}
            }, 200)
    else:
        return _json_response({'message': 'Bad request'}, 400)


@app.route('/_xhr/project/participant', methods=['POST'])
@login_required
def add_participant():
    data = request.get_json()
    if data and 'user_id' in data.keys() and 'project_id' in data.keys():
        user_id = data['user_id']
        project_id = data['project_id']
        project_controller = controllers.ProjectController()
        if not current_user.is_admin() and \
                not project_controller.is_project_head(
                    project_id=project_id,
                    user_id=current_user.get_id()
                ):
            return _json_response({'message': "You do not have head or admin rights"}, 405)

        if not controllers.UserController().get_user(user_id):
            logger.info('No such user')
            return _json_response({'message': 'No such user'}, 400)

        pp = project_controller.user_in_project(project_id=project_id, user_id=user_id)
        if pp:
            status = 200
            message = 'User already participant'
        else:
            pp = project_controller.add_user_to_project(user_id=user_id, project_id=project_id)
            if not pp:
                logger.info('No such project')
                return _json_response({'message': 'No such project'}, 400)
            status = 201
            message = 'User added to project'

        project = __project_from_participant(pp)
        logger.info('User added to project')
        return _json_response(
            {
                'message': message,
                'data': {'project': project}
            }, status)
    else:
        return _json_response({'message': 'Bad request'}, 400)


@app.route('/_xhr/users', methods=['GET'])
@login_required
def user_by_username():
    username = request.args.get('username')
    username_match = request.args.get('username_match')
    if username:
        user = controllers.UserController().get_user_by_username(username)
        return _json_response(data={
            "data": {
                "user": user
            }
        }, status_code=200 if user else 404)
    elif username_match:
        users_list = controllers.UserController().find_user_by_username(username_match)
        return _json_response(data={
            "data": {
                "users": users_list
            }
        }, status_code=200 if users_list else 404)
    else:
        return _json_response({'message': 'Bad request'}, 400)


@app.route('/_xhr/users/<string:user_id>', methods=['GET'])
@login_required
def user_by_id(user_id):
    if user_id:
        user = controllers.UserController().get_user(user_id)
        return _json_response(data={
            "data": {
                "user": user
            }
        }, status_code=200 if user else 404)
    else:
        return _json_response({'message': 'Bad request'}, 400)


@app.route('/_xhr/projects', methods=['GET'])
@login_required
def project_by_title():
    title = request.args.get('title')
    title_match = request.args.get('title_match')
    if title:
        project = controllers.ProjectController().get_project_by_title(title)
        return _json_response(data={
            "data": {
                "project": project
            }
        }, status_code=200 if project else 404)
    elif title_match:
        projects_list = controllers.ProjectController().find_project_by_title(title_match)
        return _json_response(data={
            "data": {
                "projects": projects_list
            }
        }, status_code=200 if projects_list else 404)
    else:
        return _json_response({'message': 'Bad request'}, 400)


@app.route('/_xhr/projects/<string:project_id>', methods=['GET'])
@login_required
def project_by_id(project_id):
    if project_id:
        project = controllers.ProjectController().get_project(project_id)
        return _json_response(data={
            "data": {
                "project": project
            }
        }, status_code=200 if project else 404)
    else:
        return _json_response({'message': 'Bad request'}, 400)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/me', methods=['GET'])
@login_required
def cur_user():
    user = workers.UserWorker().get_by_username(current_user.get_name())
    return _json_response(data={
        "data": {
            "user": dict(user)
        }
    })


@app.route('/users', methods=['GET'])
@login_required
def users():
    users_list = mongo.db.User.find({})
    logger.info(users_list)
    return _json_response(data={
        "data": {
            "users": list(users_list)
        }
    })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
