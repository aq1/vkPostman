import telegram
import requests

from utils.logging import vk_logger
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

POLLING_ERRORS = {
    1: (
        'the event history went out of date '
        'or was partially lost. the app can '
        'continue receiving events using the '
        'new ts value from the answer'
    ),
    2: (
        'the key’s active period expired.'
        'It\'s necessary to receive a key using '
        'the messages.getLongPollServer method'
    ),
    3: (
        'user information was lost. '
        'It\'s necessary to request a '
        'new key and ts with the help '
        'of the messages.getLongPollServer method'
    ),
    4: (
        'an invalid version number was '
        'passed in the version parameter.'
    ),
}


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
    ).json()


def start_polling(_try=0, _try_limit=3):
    if _try > _try_limit:
        vk_logger.error('Maximum retries exceeded with polling')
        return

    polling = _get_polling_server()
    if not polling:
        return start_polling(_try=_try + 1, _try_limit=_try_limit)

    polling = polling['response']
    ts = polling['ts']

    vk_logger.info('Polling with the key: {}'.format(polling['key']))

    while True:
        r = requests.get(
            'https://{}'.format(polling['server']),
            params={
                'key': polling['key'],
                'ts': ts,
                'act': 'a_check',
                'wait': 25,
                'mode': 2,
                'version': 2,
            }
        ).json()

        if r.get('failed'):
            vk_logger.info('{}: {}. {} Restarting.'.format(
                r['failed'],
                polling['key'],
                POLLING_ERRORS[r['failed']]
            ))
            return start_polling(_try=_try + 1, _try_limit=_try_limit)

        ts = r['ts']
        for u in r['updates']:
            if u[0] == 4 and not has_flag(u[2], 2):
                vk_user = vk.functions.get_vk_user(u[3])
                try:
                    vk.functions.send_message_from_vk_to_telegram(vk_user, u)
                except:
                    vk_logger.exception('vk_polling')
                    vk.api.send_message(u[3], _VK_POLLING_FAILED_MESSAGE)
                    continue


def start():
    vk_logger.info('Starting vk polling')
    telegram.Bot(token=settings.TELEGRAM_TOKEN).send_message(
        chat_id=settings.ADMIN_ID,
        text='Starting vk polling',
    )
    start_polling()


if __name__ == '__main__':
    start()
