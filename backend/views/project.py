
from flask import Blueprint, request
from flask_login import login_required, current_user

from common.json_response import json_response
from common.logger import get_logger
from common import controllers, consts

logger = get_logger(name="project-views")
project_view = Blueprint("project_view", __name__)


def __project_from_participant(pp):
    project = pp.project
    pp.project = project.id
    if pp in pp.user.projects:
        pp.user.projects.remove(pp)
        pp.user.projects.append(pp.id)
    return project


def __project_only_from_participant(pp):
    project = pp.project
    pp.project = project.id
    project.participants.remove(pp)
    project.participants.append(pp.id)
    project.head = project.head.id
    return project


@project_view.route('/_xhr/project', methods=['POST'])
@login_required
def new_project():
    if not current_user.is_admin():
        return json_response({'message': "You do not have admin rights"}, 405)
    data = request.get_json()
    if data and 'title' in data.keys():
        title = data['title']
        project_controller = controllers.ProjectController()
        if not project_controller.validate_title(title):
            logger.info('Failed title validation')
            return json_response({'message': 'Failed title validation'}, 400)
        if not project_controller.check_title_free(title):
            logger.info('Title already in use')
            return json_response({'message': 'Title already in use'}, 400)
        project = project_controller.create_project(title)
        if project:
            logger.info('Project created')
            return json_response(
                {
                    'message': 'Project created',
                    'data': {'project': project}
                }, 201)
        else:
            logger.info('Failed project creation')
            return json_response({'message': 'Project not created'}, 400)
    else:
        return json_response({'message': 'Bad request'}, 400)


@project_view.route('/_xhr/project/head', methods=['POST'])
@login_required
def set_project_head():
    if not current_user.is_admin():
        return json_response({'message': "You do not have admin rights"}, 405)
    data = request.get_json()
    if data and 'user_id' in data.keys() and 'project_id' in data.keys():
        user_id = data['user_id']
        if not controllers.UserController().get_user(user_id):
            logger.info('No such user')
            return json_response({'message': 'No such user'}, 400)
        project_id = data['project_id']
        project_controller = controllers.ProjectController()
        pp = project_controller.set_head(project_id, user_id)
        if not pp:
            logger.info('No such project')
            return json_response({'message': 'No such project'}, 400)

        project = __project_from_participant(pp)
        logger.info('Project head updated')
        return json_response(
            {
                'message': 'Project head updated',
                'data': {'project': project}
            }, 200)
    else:
        return json_response({'message': 'Bad request'}, 400)


@project_view.route('/_xhr/project/participant', methods=['POST'])
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
            return json_response({'message': "You do not have head or admin rights"}, 405)

        if not controllers.UserController().get_user(user_id):
            logger.info('No such user')
            return json_response({'message': 'No such user'}, 400)

        pp = project_controller.user_in_project(project_id=project_id, user_id=user_id)
        if pp:
            status = 200
            message = 'User already participant'
        else:
            pp = project_controller.add_user_to_project(user_id=user_id, project_id=project_id)
            if not pp:
                logger.info('No such project')
                return json_response({'message': 'No such project'}, 400)
            status = 201
            message = 'User added to project'

        project = __project_from_participant(pp)
        logger.info('User added to project')
        return json_response(
            {
                'message': message,
                'data': {'project': project}
            }, status)
    else:
        return json_response({'message': 'Bad request'}, 400)


@project_view.route('/_xhr/projects', methods=['GET'])
@login_required
def project_by_title():
    title = request.args.get('title')
    title_match = request.args.get('title_match')
    project_controller = controllers.ProjectController()
    if title:
        project = project_controller.get_project_by_title(title)
        if current_user.is_admin() or project and project_controller.user_in_project(project.id, current_user.get_id()):
            return json_response(data={
                "data": {
                    "project": project
                }
            }, status_code=200 if project else 404)
        else:
            return json_response({'message': 'Project not found or you are do not have rights for it'}, 404)
    elif title_match:
        projects_list = project_controller.find_project_by_title(title_match)
        if current_user.is_admin():
            return json_response(data={
                "data": {
                    "projects": projects_list
                }
            }, status_code=200 if projects_list else 404)
        else:
            filtered_projects = []
            for project in projects_list:
                if project_controller.user_in_project(project.id, current_user.get_id()):
                    filtered_projects.append(project)
            return json_response(data={
                "data": {
                    "projects": filtered_projects
                }
            }, status_code=200 if filtered_projects else 404)
    else:
        pps = project_controller.get_user_projects(current_user.get_id())
        projects_list = [__project_only_from_participant(pp) for pp in pps]
        return json_response(data={
            "data": {
                "projects": projects_list
            }
        }, status_code=200 if projects_list else 404)


@project_view.route('/_xhr/projects/<string:project_id>', methods=['GET'])
@login_required
def project_by_id(project_id):
    if project_id:
        project_controller = controllers.ProjectController()
        if current_user.is_admin() or project_controller.user_in_project(project_id, current_user.get_id()):
            project = project_controller.get_project(project_id)
            if project:
                tasks = []
                tc = controllers.TaskController()
                for task in project.tasks:
                    tsk = tc.get_task(task)
                    if tsk:
                        tasks.append(tsk)
                project.tasks = tasks
                pps = []
                for _pp in project.participants:
                    pp = project_controller.get_project_participant(_pp)
                    pp.project = pp.project.id
                    pp.user.projects = []
                    if _pp:
                        pps.append(pp)
                project.participants = pps
                pp = project_controller.get_project_participant(project.head)
                pp.project = pp.project.id
                pp.user.projects = []
                project.head = pp
                return json_response(data={
                    "data": {
                        "project": project
                    }
                }, status_code=200 if project else 404)
        else:
            return json_response({'message': 'Project not found or you are do not have rights for it'}, 404)
    else:
        return json_response({'message': 'Bad request'}, 400)


@project_view.route('/_xhr/projects/participant/<string:pp_id>', methods=['GET'])
@login_required
def pp_by_id(pp_id):
    if pp_id:
        project_controller = controllers.ProjectController()
        pp = project_controller.get_project_participant(pp_id)
        if pp and current_user.is_admin() or project_controller.user_in_project(pp.project.id, current_user.get_id()):
            pp.project = pp.project.id
            pp.user.projects = []
            return json_response(data={
                "data": {
                    "pp": pp
                }
            }, status_code=200 if pp else 404)
        else:
            return json_response({'message': 'Project participant not found or you are do not have rights for it'}, 404)
    else:
        return json_response({'message': 'Bad request'}, 400)


@project_view.route('/_xhr/projects/<string:project_id>/<string:action>', methods=['POST'])
@login_required
def project_status_action(project_id, action):
    try:
        action = consts.ProjectAction[action]
    except KeyError:
        return json_response({'message': 'Unknown action'}, 400)

    project_controller = controllers.ProjectController()
    project = project_controller.get_project(project_id)
    if not project:
        return json_response({'message': 'Project not found'}, 404)
    project = project_controller.perform_action(project=project, user_id=current_user.get_id(), action=action)
    if not project:
        return json_response({'message': 'You cannot perform this action'}, 405)

    return json_response({
        'message': 'ok',
        'data': {
            'project': project
        }
    }, 200)
