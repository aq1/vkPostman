from django.conf import settings

import requests

from chat.models import Chat
from chat.telegram.commands import CommandBase


def send_message_to_telegram_user(data):
    """
    data[0]: event type
    data[1]: message_id
    data[2]: mask
    data[3]: peer_id
    data[4]: timestamp
    data[5]: text
    data[6]: extra?
    """
    try:
        chat = Chat.objects.get(vk_user_id=data[3], is_active=True)
    except Chat.DoesNotExist:
        return

    CommandBase.send_message(chat.telegram_user_id, text=data[5])


def send_message_to_vk_user(telegram_user_id, message):
    try:
        chat = Chat.objects.get(telegram_user_id=telegram_user_id, is_active=True)
    except Chat.DoesNotExist:
        return

    url = 'https://api.vk.com/method/messages.send'
    requests.post(url, data={
        'user_id': chat.vk_user_id,
        'message': message,
        'access_token': settings.VK_TOKEN,
    })
