import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOGS_PATH = os.path.join(BASE_DIR, 'logs')


DEBUG = False

MONGO_HOST = ''
MONGO_PORT = ''
MONGO_DB = ''
MONGO_USER = ''
MONGO_PASSWORD = ''

TELEGRAM_TOKEN = ''

VK_TOKEN = ''
VK_API_VERSION = 5.74

ADMIN_ID = ''

SENTRY_URL = ''
