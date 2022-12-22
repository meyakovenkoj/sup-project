import os
import simplejson as json

from flask import Blueprint, request

from common.logger import get_logger
from common.conf import config

logger = get_logger(name="zaglushka-views")
zaglushka_view = Blueprint("zaglushka_view", __name__)


@zaglushka_view.route('/_xhr/start_test_zaglushka', methods=['POST'])
def start_test():
    data = request.get_json()
    logger.info(f'TESTING DATA: {data}')
    with open(os.path.join(config.ATTACHMENTS_ROOT, 'zaglushka.txt'), 'a') as f:
        f.write(json.dumps(data) + '\r\n')
