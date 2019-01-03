import requests

import settings


URL = 'https://api.vk.com/method/{}'


def call(method, api_method, data=None, params=None):
    r = getattr(requests, method)
    data = data or {}
    params = params or {}
    params['access_token'] = settings.VK_TOKEN
    params['v'] = settings.VK_API_VERSION
    return r(URL.format(api_method), data=data, params=params)


def get_user(user_id):
    r = call('get', 'users.get', params={'user_ids': user_id})
    try:
        return r.json()['response'][0]
    except (ValueError, IndexError):
        return


def send_message(vk_id, message):
    return call(
        'post',
        'messages.send',
        data={
            'user_id': vk_id,
            'message': message,
            # 'attachment': attachment,
        }
    )
