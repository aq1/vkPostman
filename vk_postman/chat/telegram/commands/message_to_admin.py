from django.conf import settings

from chat.vk import vk_chat
from chat.telegram.commands import CommandBase


class MessageToAdmin(CommandBase):

    _description = 'Write to admin.'
    _SUCCESS_MSG = 'Message sent'

    @staticmethod
    def _format_message(from_, message):
        return 'Message from user "{} {}" to admin.\n{}'.format(
            from_['first_name'],
            from_['last_name'],
            message,
        )

    @classmethod
    def _execute(cls, from_, args):
        try:
            message = args[0]
        except IndexError:
            return False, 'Message is required.'

        message = cls._format_message(from_, message)
        vk_chat.send_message_to_vk_user(settings.ADMIN_ID, message)
        return True, None
