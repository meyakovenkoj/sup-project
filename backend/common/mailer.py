import typing

from flask_mail import Mail, Message

from common.conf import config
from common import base
from common.logger import get_logger

logger = get_logger("mailer")


mail = Mail()


def send_message(message, to_users: typing.List[base.User]):
    try:
        recipients = [f'{user.username}{config.MAIL_SUFFIX if "@" not in user.username else ""}' for user in to_users]
        logger.info(f'Sending messages')
        msg = Message('Sup notification', sender=config.MAIL_USERNAME, recipients=recipients)
        msg.body = message
        mail.send(msg)
    except Exception as e:
        logger.error(f'Message not sent with error {e}')
    else:
        logger.info(f'Messages sent')
