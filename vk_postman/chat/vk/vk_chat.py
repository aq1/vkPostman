import requests

from chat.models import Chat
from chat.telegram import telegram_api
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
    telegram_api.call(
        'sendMessage',
        data={
            'chat_id': chat.telegram_user_id,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True,
        }
    )
    vk_api.call(
        'post',
        'messages.markAsRead',
        data={
            'user_id': vk_user_id,
        }
    )


def send_message_to_vk_user(vk_user_id, message, attachment=None):
    vk_api.call(
        'post',
        'messages.send',
        data={
            'user_id': vk_user_id,
            'message': message,
            'attachment': attachment,
        }
    )


def upload_photo_from_telegram_to_vk(photo):

    photo_file_path = telegram_api.call(
        'getFile',
        data={
            'file_id': photo[3]['file_id'],
        }
    ).json()['result']['file_path']

    photo_file = telegram_api.get_file(photo_file_path)
    upload_url = vk_api.call(
        'get',
        'photos.getMessagesUploadServer',
    ).json()['response']['upload_url']

    vk_photo = requests.post(
        upload_url,
        files={
            'photo': (
                photo_file_path,
                photo_file.raw,
                {'Content-Type': photo_file.headers.get('Content-Type', 'application/octet-stream')},
            ),
        }
    )
    return vk_api.call(
        'post',
        'photos.saveMessagesPhoto',
        data=vk_photo.json(),
    )


def send_message_from_telegram_to_vk(data):
    if not data.get('message'):
        return

    telegram_user_id = data['message']['from']['id']

    try:
        chat = Chat.objects.select_related('telegram_user').get(
            telegram_user_id=telegram_user_id,
            telegram_active=True,
            vk_active=True,
        )
    except Chat.DoesNotExist:
        return

    photo = data['message'].get('photo')
    attachment = None
    # document = data['message'].get('document')
    if photo:
        text = data['message'].get('caption', '')
        attachment = upload_photo_from_telegram_to_vk(photo).json()['response'][0]['id']
    else:
        text = data['message'].get('text', '')

    message = '{} {}:\n{}'.format(
        chat.telegram_user.first_name,
        chat.telegram_user.last_name,
        text,
    )
    send_message_to_vk_user(chat.vk_user_id, message, attachment=[attachment])
