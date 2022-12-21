import os

from flask import Blueprint, request, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from common import controllers, consts
from common.logger import get_logger
from common.json_response import json_response
from common import file_worker as fw
from common.conf import config

logger = get_logger(name="task-views")
task_view = Blueprint("task_view", __name__)


def __do_upload(file, folder_name, parent_folder=None):
    upload_to = fw.create_upload_folder(name=folder_name, parent_folder=parent_folder)
    logger.debug(f'Upload folder: {upload_to}')
    filename = secure_filename(file.filename)
    logger.debug(f'File: {filename}')
    fw.create_if_not_exists(upload_to)
    file.save(os.path.join(upload_to, filename))
    return upload_to


def __check_request_file(check_file_existence=True, check_extension=True):
    # Check file sent in request
    if check_file_existence and 'file' not in request.files:
        return 'Need to send file!', 403
    # Check file available and valid
    file = request.files['file']
    if not file:
        return 'File cannot be empty!', 403
    elif file.filename == '':
        return 'File name cannot be empty!', 403
    # elif check_extension and not fw.allowed_file(file.filename):
    #     return 'File extension not allowed!', 403
    else:
        return file, None


def __task_from_subscriber(ts):
    pp = ts.subscriber

    project = pp.project
    pp.project = project.id
    if pp in pp.user.projects:
        pp.user.projects.remove(pp)
        pp.user.projects.append(pp.id)

    task = ts.task
    ts.task = task.id
    if ts in ts.subscriber.subscriptions:
        ts.subscriber.subscriptions.remove(ts)
        ts.subscriber.subscriptions.append(ts.id)
    return project


@task_view.route('/_xhr/tasks', methods=['POST'])
@login_required
def new_task():
    # if not current_user.is_admin():
    #     return json_response({'message': "You do not have admin rights"}, 405)
    data = request.get_json()
    if data and 'title' in data.keys() and 'description' in data.keys() and 'task_type' in data.keys() and 'project_id' in data.keys():
        project_id = data['project_id']
        project_controller = controllers.ProjectController()
        pp = project_controller.user_in_project(project_id=project_id, user_id=current_user.get_id())

        if not pp:
            return json_response({'message': 'Project not found or you cannot create tasks in this project'}, 404)

        title = data['title']
        description = data['description']

        try:
            task_type = consts.TaskType[data['task_type']]
        except KeyError:
            return json_response({'message': 'Unknown task_type'}, 400)

        task_controller = controllers.TaskController()
        if not task_controller.validate_data(title, description):
            logger.info('Failed title validation')
            return json_response({'message': 'Failed title validation'}, 400)

        if not task_controller.check_title_free(title):
            logger.info('Title already in use')
            return json_response({'message': 'Title already in use'}, 400)

        ts = task_controller.create_task(
            title=title,
            description=description,
            task_type=task_type,
            project_id=project_id,
            author_id=pp.id
        )
        if ts:
            logger.info('Task created')
            task = __task_from_subscriber(ts)
            return json_response(
                {
                    'message': 'Task created',
                    'data': {'task': task}
                }, 201)
        else:
            logger.info('Failed task creation')
            return json_response({'message': 'Task not created'}, 400)
    else:
        return json_response({'message': 'Bad request'}, 400)
    

@task_view.route('/_xhr/tasks/<string:task_id>/attach', methods=['POST'])
@login_required
def upload_file(task_id):
    file, file_status = __check_request_file()
    if file_status:
        return file, file_status

    task_controller = controllers.TaskController()
    task = task_controller.get_task(task_id)
    if not task:
        return 'Task not found', 404

    project_controller = controllers.ProjectController()
    pp = project_controller.user_in_project(project_id=task.project, user_id=current_user.get_id())

    if not pp:
        return json_response({'message': 'Task not found or you cannot update tasks in this project'}, 404)

    if task and file:
        task = task_controller.attach_files(
            task.id,
            __do_upload(file, folder_name=str(task.id))
        )
    if task:
        return json_response({'message': "Files uploaded", 'data': {'task': task}}, 200)
    return 'Upload failed', 400


@task_view.route('/attachments/<string:project_id>/<string:task_id>/<string:filename>', methods=['GET'])
@login_required
def download_attachment(project_id, task_id, filename):
    task = controllers.TaskController().get_task(task_id)
    if task and str(task.project) == project_id:
        pp = controllers.ProjectController().user_in_project(project_id=project_id, user_id=current_user.get_id())
        if pp:
            uploads = os.path.join(config.ATTACHMENTS_ROOT, project_id, task_id)
            return send_from_directory(directory=uploads, path=filename)
    return json_response({'message': 'No such task or project or you do not have such rights'}, 404)