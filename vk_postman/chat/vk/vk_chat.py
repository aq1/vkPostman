from chat.models import Chat
from chat.telegram.commands import CommandBase
from chat.vk import vk_api


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
        chat = Chat.objects.select_related('vk_user').get(
            vk_user_id=vk_user_id,
            vk_active=True,
        )
    except Chat.DoesNotExist:
        send_message_to_vk_user(vk_user_id, 'Sorry! No active chats found for you.')
        return
    except Chat.MultipleObjectsReturned:
        send_message_to_vk_user(vk_user_id, 'Sorry! Multiple telegram users are connected to you.')
        return

    text = '<b>{} {}</b>\n{}'.format(
        chat.vk_user.first_name,
        chat.vk_user.last_name,
        data[5],
    )
    CommandBase.send_message(chat.telegram_user_id, text=text)
    vk_api.call(
        'post',
        'messages.markAsRead',
        data={
            'user_id': vk_user_id,
        }
    )


def send_message_to_vk_user(vk_user_id, message):
    vk_api.call(
        'post',
        'messages.send',
        data={
            'user_id': vk_user_id,
            'message': message,
        }
    )


def send_message_from_telegram_to_vk(telegram_user_id, message, photo=None):
    try:
        chat = Chat.objects.select_related('telegram_user').get(
            telegram_user_id=telegram_user_id,
            telegram_active=True,
            vk_active=True,
        )
    except Chat.DoesNotExist:
        return

    message = '{} {}:\n{}'.format(
        chat.telegram_user.first_name,
        chat.telegram_user.last_name,
        message
    )
    send_message_to_vk_user(chat.vk_user_id, message)
