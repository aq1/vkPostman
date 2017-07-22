from django.conf import settings

import requests


class CommandBase:

    description = ''

    @staticmethod
    def send_message(telegram_user_id, text):
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(settings.TELEGRAM_TOKEN)
        return requests.post(url, data={'chat_id': telegram_user_id, 'text': text, 'parse_mode': 'Markdown'})

    @classmethod
    def execute(cls, telegram_user_id, *args):
        raise NotImplementedError
