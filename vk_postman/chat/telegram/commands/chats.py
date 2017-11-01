import json

from chat.models import Chat

from chat.telegram.commands import CommandBase


class Chats(CommandBase):

    _description = 'Show my chats.'
    _SUCCESS_MSG = ''

    @classmethod
    def _execute(cls, from_, args):
        chats = Chat.objects.filter(telegram_user_id=from_['id']).select_related('vk_user').order_by('telegram_active')
        if not chats:
            return cls._execution_result(True, 'No chats history. Connect to a user and his name will be shown here.')
        reply_markup = []
        for chat in chats:
            text = '{} {}'.format(
                chat.vk_user.last_name,
                chat.vk_user.first_name,
            )
            if chat.is_active():
                text = '\U00002705 {}'.format(text)

            reply_markup.append([
                {
                    'text': text,
                    'callback_data': '/connect {}'.format(chat.vk_user_id)
                },
                {
                    'text': '\U0000274C',
                    'callback_data': '/remove_chat {}'.format(chat.vk_user_id)
                },
            ])

        return cls._execution_result(
            True,
            'Your chats. Click name to connect. Click X to remove chat from history.',
            reply_markup=json.dumps({'inline_keyboard': reply_markup})
        )
