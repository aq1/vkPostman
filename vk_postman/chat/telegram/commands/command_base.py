from django.conf import settings

import requests


class CommandBase:

    description = ''
    _SUCCESS_MSG = ''
    _send_feedback = False

    @staticmethod
    def _get_vk_user_url(vk_user_id):
        return 'https://vk.com/id{}'.format(vk_user_id)

    @classmethod
    def _create_success_message(cls, args):
        try:
            vk_user = cls._get_vk_user_url(args[0])
        except IndexError:
            vk_user = ''
        return cls._SUCCESS_MSG.format(vk_user=vk_user)

    @classmethod
    def _execute(cls, telegram_user_id, *args):
        return True, None

    @staticmethod
    def send_message(telegram_user_id, text):
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(settings.TELEGRAM_TOKEN)
        return requests.post(url, data={'chat_id': telegram_user_id, 'text': text, 'parse_mode': 'Markdown'})

    @classmethod
    def execute(cls, telegram_user_id, *args):
        result, msg = cls._execute(telegram_user_id, *args)
        if msg is None:
            msg = cls._create_success_message(args)

        cls.send_message(telegram_user_id, msg)
