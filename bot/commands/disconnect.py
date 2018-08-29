from bot.commands import BaseCommand

import mongo


class DisconnectCommand(BaseCommand):

    _COMMAND = 'disconnect'
    _DESCRIPTION = 'Close currently active chat.'
    _SUCCESS_MESSAGE = 'Disconnected from all chats'

    def _callback(self, user, _bot, update, **kwargs):
        return self._call(user, _bot, update, **kwargs)

    def _call(self, user, _bot, update, **kwargs):
        chat = mongo.chats.get_active_chat_by_telegram_id(user.id)
        if chat:
            mongo.chats.disable_chat(chat['_id'])
            return True
        _bot.send_message(
            user.id,
            'You are not connected to any vk user',
        )
