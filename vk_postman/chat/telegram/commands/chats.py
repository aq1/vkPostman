import json

from chat.models import Chat

from chat.telegram.commands import CommandBase


class Chats(CommandBase):

    _description = 'Show my chats.'
    _SUCCESS_MSG = ''

    @classmethod
    def _execute(cls, from_, args):
        chats = Chat.objects.filter(telegram_user_id=from_['id']).select_related('vk_user').order_by('telegram_active')
        result = []
        for chat in chats:
            text = '{} {}'.format(
                chat.vk_user.last_name,
                chat.vk_user.first_name,
            )
            if chat.is_active():
                text = '\U00002705 {}'.format(text)

            result.append([
                {
                    'text': text,
                    'callback_data': 'Nope'
                },
                {
                    'text': '\U0000274C {:>15}'.format(chat.vk_user_id),
                    'callback_data': 'Nope'
                },
            ])

        result = json.dumps({
            'inline_keyboard': result
        })
        return cls._execution_result(True, 'Your chats click to connect:', reply_markup=result)
