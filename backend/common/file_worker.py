import os
import random
import string
from datetime import datetime
from shutil import move, rmtree

from common.logger import get_logger
from common.conf import config
from common.base import Task, Project


logger = get_logger('file-utils')


def create_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)


def rm_folder(folder):
    try:
        rmtree(folder)
        logger.info(f'Folder - {folder} was deleted')
    except FileNotFoundError:
        logger.info('File not found: {}'.format(folder))


def get_relative_path(full_path):
    return full_path.replace(config.ATTACHMENTS_ROOT, '')


def get_ses_id(session: dict, renew=None):
    if renew:
        return __generate_session_key()
    elif config.SID_KEY not in session.keys() or not session[config.SID_KEY]:
        return __generate_session_key()
    else:
        return session[config.SID_KEY]


def __generate_session_key():
    rnd = ''.join(random.sample(string.ascii_lowercase + string.digits, 10))
    return datetime.now().strftime('%Y%m%d%H%M%S%f') + rnd


def get_folder(name=None, parent=None):
    if parent is None:
        parent = config.UPLOAD_FOLDER
    return os.path.join(str(parent), str(name) if name else __generate_session_key())


def create_upload_folder(name=None, parent_folder=None):
    upload_folder = get_folder(name, parent=parent_folder)
    logger.debug('Upload folder: {}'.format(upload_folder))
    create_if_not_exists(upload_folder)
    return upload_folder


class ResultWorkerException(Exception):
    pass


class FileWorker:
    def __init__(self, task: Task):
        self.task = task

    def _collect_place_path(self):
        try:
            if isinstance(self.task.project, Project):
                p_id = self.task.project.id
            else:
                p_id = self.task.project
            return os.path.join(config.ATTACHMENTS_ROOT, str(p_id), str(self.task.id))
        except Exception as e:
            raise ResultWorkerException(f'Cannot collect path from task object: {e}')

    def move_arts(self, from_folder):
        move_to = None
        try:
            move_to = self._collect_place_path()
            create_if_not_exists(move_to)
            for f in os.listdir(from_folder):
                move(os.path.join(from_folder, f), move_to)
            rm_folder(from_folder)
        except ResultWorkerException as e:
            logger.error(f'Cannot move from "{from_folder}" to unknown folder.\n{e}')
        except OSError as e:
            logger.debug(e)
        except Exception as e:
            logger.debug(f'Unknown exception: {e}')
        finally:
            return move_to

    def make(self, from_folder):
        arts = self.move_arts(from_folder)
        attach_paths = []
        if not arts:
            logger.error('Error occurred while moving data. Need another attempt or admin help')
            return None
        for f in os.listdir(arts):
            art_path = os.path.join(arts, f)
            attach_paths.append(get_relative_path(art_path))
        return attach_paths
