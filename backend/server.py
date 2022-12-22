import secrets

from pathlib import Path
from flask import Flask, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from flask_cors import CORS

from common.conf import config
from common.json_response import json_response
from common.logger import get_logger
from common import workers, controllers
from common.mailer import mail

from views.task import task_view
from views.project import project_view
from views.user import user_view


logger = get_logger(name='main-server')
app = Flask(__name__, static_url_path='/static', template_folder='/template')
CORS(app, supports_credentials=True)

# register views
app.register_blueprint(task_view)
app.register_blueprint(project_view)
app.register_blueprint(user_view)

#zaglushka
if 'localhost' in config.TEST_SERVER_URL:
    from views.zaglushka import zaglushka_view
    app.register_blueprint(zaglushka_view)

app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PWD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

app.config["MONGO_URI"] = config.MONGO_URI
mongo = PyMongo(app)
mail.init_app(app)

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


# XXX for pokaz
@app.route('/_projects', methods=['GET'])
@login_required
def projects():
    projects_list = mongo.db.Project.find({})
    logger.info(projects_list)
    return json_response(data={
        "data": {
            "projects": list(projects_list)
        }
    })

@app.route('/_tasks', methods=['GET'])
@login_required
def tasks():
    tasks_list = mongo.db.Task.find({})
    logger.info(tasks_list)
    return json_response(data={
        "data": {
            "tasks": list(tasks_list)
        }
    })



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
