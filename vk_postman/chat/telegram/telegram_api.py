import requests

from django.conf import settings


URL = 'https://api.telegram.org/bot{}/{{}}'.format(settings.TELEGRAM_TOKEN)
FILE_URL = 'https://api.telegram.org/file/bot{}/{{}}'.format(settings.TELEGRAM_TOKEN)


def call(api_method, data=None):
    data = data or {}
    return requests.post(URL.format(api_method), data=data)


def get_file(path):
    return requests.get(FILE_URL.format(path), stream=True)
