from django.conf import settings

import requests

from chat.vk.vk_chat import send_message_to_telegram_user


def _get_polling_server():
    return requests.get(
        'https://api.vk.com/method/messages.getLongPollServer?access_token={}'.format(
            settings.VK_TOKEN
        )
    ).json()['response']


def watch_chat():
    polling = _get_polling_server()
    ts = polling['ts']
    while True:
        r = requests.get('https://{}?act=a_check&key={}&ts={}&wait=25&mode=2&version=2'.format(polling['server'], polling['key'], ts)).json()
        ts = r['ts']
        for u in r['updates']:
            if u[0] == 4:
                send_message_to_telegram_user(u)
