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
ADMIN_ID = os.environ.get('ADMIN_ID', '')

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')
ADMINS = (
    ('admin', os.environ.get('ADMIN_EMAIL')),
)
