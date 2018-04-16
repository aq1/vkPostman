import requests

from django.conf import settings


URL = 'https://api.vk.com/method/{}'


def call(method, api_method, data=None, params=None):
    r = getattr(requests, method)
    data = data or {}
    params = params or {}
    params['access_token'] = settings.VK_TOKEN
    params['v'] = settings.VK_API_VERSION
    return r(URL.format(api_method), data=data, params=params)
