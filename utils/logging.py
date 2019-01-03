import os
import logging
from logging.handlers import TimedRotatingFileHandler

import settings

logger = logging.getLogger('Bot Log')
logger.setLevel(logging.INFO)

path = os.path.join(settings.LOGS_PATH, 'bot_log.log')
os.makedirs(settings.LOGS_PATH, exist_ok=True)
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
logger.addHandler(handler)
