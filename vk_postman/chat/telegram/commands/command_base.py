import re

from django.conf import settings

import requests


class StrMC(type):
    """
    Class creates neat string representaion for himself,
    not for it instances only.
    Also, changes class name to underscore.
    """

    def __new__(cls, class_name, *args, **kwargs):
        class_name = re.sub(r'([A-Z]{1})', r'_\1', class_name).lower().lstrip('_')
        return super().__new__(cls, class_name, *args, **kwargs)

    def __str__(cls):
        return '{} - {}'.format(cls.__name__, cls._description)


class CommandBase(metaclass=StrMC):
    _description = ''
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
    def _execute(cls, from_, args):
        return True, None

    @staticmethod
    def send_message(telegram_user_id, text, parse_mode='HTML', disable_web_page_preview=True):
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(settings.TELEGRAM_TOKEN)
        return requests.post(
            url,
            data={
                'chat_id': telegram_user_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': disable_web_page_preview
            },
        )

    @classmethod
    def execute(cls, from_, args):
        result, msg = cls._execute(from_, args)
        if msg is None:
            msg = cls._create_success_message(args)
            if not msg:
                return
        print(result, msg)
        cls.send_message(from_['id'], msg)
