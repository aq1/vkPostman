from bot.commands import BaseCommand

import mongo


class DisconnectCommand(BaseCommand):

    _COMMAND = 'disconnect'
    _DESCRIPTION = 'Close currently active chat.'
    _SUCCESS_MESSAGE = 'Disconnected from all chats'

    def _call(self, bot, update, **kwargs):
        chat = mongo.get_active_chat_by_telegram_id(update.message.chat.id)
        if chat:
            mongo.disable_chat(chat['_id'])
            return True
        update.message.reply_text('You are not connected to any vk user')
