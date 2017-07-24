from chat.models import Chat

from chat.telegram.commands import CommandBase


class Chats(CommandBase):

    _description = 'Show my chats'
    _SUCCESS_MSG = ''

    @classmethod
    def _execute(cls, telegram_user_id, *args):
        chats = Chat.objects.filter(telegram_user_id=telegram_user_id).order_by('telegram_active')
        result = []
        for chat in chats:
            s = cls._get_vk_user_url(chat.vk_user_id)
            if chat.is_active():
                s = '{} - active'.format(s)
            result.append(s)

        return True, '\n'.join(result)
