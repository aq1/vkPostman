from django.conf import settings

import requests

from chat.models import Chat
from chat.telegram.commands import CommandBase


def send_message_from_vk_to_telegram(data):
    """
    data[0]: event type
    data[1]: message_id
    data[2]: mask
    data[3]: peer_id
    data[4]: timestamp
    data[5]: text
    data[6]: extra?
    """
    vk_user_id = data[3]
    try:
        chat = Chat.objects.get(
            vk_user_id=vk_user_id,
            telegram_active=True,
            vk_active=True,
        )
    except Chat.DoesNotExist:
        send_message_to_vk_user(vk_user_id, 'Sorry! No active chats found for you.')
    except Chat.MultipleObjectsReturned:
        send_message_to_vk_user(vk_user_id, 'Sorry! Multiple telegram users are connected to you.')

    CommandBase.send_message(chat.telegram_user_id, text=data[5])


def send_message_to_vk_user(vk_user_id, message):
    url = 'https://api.vk.com/method/messages.send'
    requests.post(url, data={
        'user_id': vk_user_id,
        'message': message,
        'access_token': settings.VK_TOKEN,
    })


def send_message_from_telegram_to_vk(telegram_user_id, message):
    try:
        chat = Chat.objects.get(
            telegram_user_id=telegram_user_id,
            telegram_active=True,
            vk_active=True,
        )
    except Chat.DoesNotExist:
        return

    send_message_to_vk_user(chat.vk_user_id, message)
