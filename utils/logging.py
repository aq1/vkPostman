import os
import logging
from logging.handlers import TimedRotatingFileHandler

import settings

os.makedirs(settings.LOGS_PATH, exist_ok=True)


def create_logger(name):
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.INFO)

    path = os.path.join(settings.LOGS_PATH, name.replace(' ', '_'))
    if not os.path.exists(path):
        f = open(path, 'w')
        f.close()

    handler = TimedRotatingFileHandler(
        path,
        when='d',
        interval=1,
        backupCount=5
    )
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    return _logger


bot_logger = create_logger('bot')
vk_logger = create_logger('vk')
