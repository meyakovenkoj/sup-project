import secrets

from pathlib import Path
from flask import Flask, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo

from common.conf import config
from common.json_response import json_response
from common.logger import get_logger
from common import workers, controllers

from views.task import task_view
from views.project import project_view


logger = get_logger(name='main-server')
app = Flask(__name__, static_url_path='/static', template_folder='/template')


# register views
app.register_blueprint(task_view)
app.register_blueprint(project_view)



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


@login_manager.user_loader
def load_user(user_id):
    return controllers.AuthorizationController().get_user(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return json_response({'message': 'Login required'}, 401)


@app.route('/_xhr/login', methods=['POST'])
def login():
    credentials = request.get_json()
    if credentials and 'username' in credentials.keys() and 'password' in credentials.keys():
        user = controllers.AuthorizationController().login_user(credentials['username'], credentials['password'])
        if user:
            login_user(user)
            logger.info(f'Successful login for user: {user.get_name()}')
            return json_response({'message': 'Successful login'}, 200)
        else:
            logger.info('Failed authorization')
            return json_response({'message': 'Wrong credentials'}, 401)
    else:
        return json_response({'message': 'Bad request'}, 400)


@app.route('/_xhr/register', methods=['POST'])
def register():
    credentials = request.get_json()
    if credentials and 'username' in credentials.keys() and 'password' in credentials.keys() and 'name' in credentials.keys() and 'surname' in credentials.keys():
        _auth_controller = controllers.AuthorizationController()
        username, password, name, surname = credentials['username'], credentials['password'], credentials['name'], credentials['surname']
        if not _auth_controller.check_username_free(username):
            logger.info('Username already in use')
            return json_response({'message': 'Username already in use'}, 400)
        if not _auth_controller.validate_creds(username, password, name, surname):
            logger.info('Failed creds validation')
            return json_response({'message': 'Failed creds validation'}, 400)
        user = _auth_controller.register(username, password, name, surname)
        if user:
            login_user(user)
            logger.info(f'Successful register and login for user: {user.get_name()}')
            return json_response({'message': 'Successful register'}, 201)
        else:
            logger.info('Failed register')
            return json_response({'message': 'Wrong credentials'}, 401)
    else:
        return json_response({'message': 'Bad request'}, 400)


@app.route('/_xhr/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return json_response({'message': 'Successful logout'}, 200)


@app.route('/_xhr/users', methods=['GET'])
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


@app.route('/_xhr/users/<string:user_id>', methods=['GET'])
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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/me', methods=['GET'])
@login_required
def cur_user():
    user = workers.UserWorker().get_by_username(current_user.get_name())
    return json_response(data={
        "data": {
            "user": dict(user)
        }
    })


@app.route('/users', methods=['GET'])
@login_required
def users():
    users_list = mongo.db.User.find({})
    logger.info(users_list)
    return json_response(data={
        "data": {
            "users": list(users_list)
        }
    })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
