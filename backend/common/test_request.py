from requests import session

from common.conf import config


def request_test(data):
    sess = session()
    sess.post(config.TEST_SERVER_URL, json=data)
