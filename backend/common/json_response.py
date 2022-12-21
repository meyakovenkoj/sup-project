import simplejson as json
from bson import ObjectId
from flask import Response, abort

from common.logger import get_logger


logger = get_logger(name="json-response")


def json_response(data, status_code=200):
    try:
        return Response(response=json.dumps(data, default=my_serializer), status=status_code,
                        mimetype='application/json')
    except Exception as e:
        logger.exception(f'Json serialize error: {e}')
        abort(400, 'Invalid json')


def my_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return dict(obj)
