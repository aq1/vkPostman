import os
import dj_database_url


SECRET_KEY = os.environ.get('SECRET_KEY')

if os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = [os.environ['ALLOWED_HOSTS']]


DATABASES = {
    'default': dj_database_url.config(),
}

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
VK_TOKEN = os.environ.get('VK_TOKEN', '')
