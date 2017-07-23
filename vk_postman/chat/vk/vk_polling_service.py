from django.conf import settings

import requests

from chat.vk.vk_chat import send_message_to_telegram_user


MESSAGE_FLAGS = [
    65536,  # HIDDEN
    512,    # MEDIA
    256,    # FIXED
    128,    # DELETED
    64,     # SPAM
    32,     # FRIENDS
    16,     # CHAT
    8,      # IMPORTANT
    4,      # REPLIED
    2,      # OUTBOX
    1,      # UNREAD
]


def has_flag(value, flag):
    while value > 0:
        for f in MESSAGE_FLAGS:
            if f <= value:
                if f == flag:
                    return True
                value -= f
    return False


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
            if u[0] == 4 and not has_flag(u[2], 2):
                send_message_to_telegram_user(u)
