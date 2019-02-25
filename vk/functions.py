import functools

import telegram

import vk
import mongo
import settings
from utils.logging import logger


_CHECK_MESSAGE = '🤔 VK polling operational'


@functools.lru_cache()
def get_vk_user(vk_id):
    vk_user = mongo.users.get_vk_user(vk_id)
    if not vk_user:
        vk_user = mongo.users.save_vk_user(vk.api.get_user(vk_id))
    return vk_user


def get_history(vk_id):
    return vk.api.call(
        'post',
        'messages.getHistory',
        data={
            'user_id': vk_id,
            'rev': 0,
        }).json()


def send_message_from_vk_to_telegram(vk_user, data):
    """
    data[0]: event type
    data[1]: message_id
    data[2]: mask
    data[3]: peer_id
    data[4]: timestamp
    data[5]: text
    data[6]: extra?
    """
    text = data[5]

    chat = mongo.chats.get_active_chat_by_vk_id(vk_user['id'])

    # If more commands will occur, this will be refactored
    if text == '/check':
        chat = {'telegram_id': settings.ADMIN_ID}
        text = _CHECK_MESSAGE

    if not chat:
        vk.api.send_message(vk_user['id'], 'Sorry! No active chats found for you.')
        return

    text = '<b>{} {}</b>\n{}'.format(
        vk_user['first_name'],
        vk_user['last_name'],
        text,
    )
    telegram.Bot(token=settings.TELEGRAM_TOKEN).send_message(
        chat_id=chat['telegram_id'],
        text=text,
        parse_mode='HTML',
        disable_web_page_preview=True,
    )
    vk.api.call(
        'post',
        'messages.markAsRead',
        data={
            'user_id': vk_user['id'],
        }
    )

    logger.info('Sent message to telegram {}'.format(chat['telegram_id']))
