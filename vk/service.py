import telegram
import requests
import mongo

from utils.logging import logger
import settings
import vk


_VK_POLLING_FAILED_MESSAGE = 'Sorry. Something went wrong. We are investigating.'
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
    vk_id = data[3]
    chat = mongo.chats.get_active_chat_by_vk_id(vk_id)
    if not chat:
        vk.api.send_message(vk_id, 'Sorry! No active chats found for you.')
        return

    vk_user = mongo.users.get_vk_user(vk_id)
    text = '<b>{} {}</b>\n{}'.format(
        vk_user['first_name'],
        vk_user['last_name'],
        data[5],
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
            'user_id': vk_id,
        }
    )

    logger.info('Sent message to telegram {}'.format(chat['telegram_id']))


def has_flag(value, flag):
    while value > 0:
        for f in MESSAGE_FLAGS:
            if f <= value:
                if f == flag:
                    return True
                value -= f
    return False


def _get_polling_server():
    return vk.api.call(
        'post',
        'messages.getLongPollServer',
    ).json()['response']


def start(_try=0, _try_limit=3):
    if _try > _try_limit:
        logger.error('Maximum retries exceeded with polling')
        return

    logger.info('Starting vk polling')
    polling = _get_polling_server()
    ts = polling['ts']
    while True:
        r = requests.get(
            'https://{}?act=a_check&key={}&ts={}&wait=25&mode=2&version=2'.format(
                polling['server'],
                polling['key'],
                ts,
            )
        ).json()

        if r.get('failed'):
            logger.info('vk poll returned error: {}. Restarting.'.format(r['failed']))
            return start(_try=_try + 1)

        ts = r['ts']
        for u in r['updates']:
            if u[0] == 4 and not has_flag(u[2], 2):
                try:
                    send_message_from_vk_to_telegram(u)
                except:
                    logger.exception('vk_polling')
                    vk.api.send_message(u[3], _VK_POLLING_FAILED_MESSAGE)
                    continue


if __name__ == '__main__':
    start()
