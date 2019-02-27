import json

import telegram.ext

from utils.logging import bot_logger

import mongo
import bot
import vk


class TransportMessageToVK(telegram.ext.RegexHandler):

    _PATTERN = '.*?'

    def __init__(self, **kwargs):

        super().__init__(
            pattern=self._PATTERN,
            callback=self.__call__,
            **kwargs
        )

    @staticmethod
    def _format_message(user, message):
        return '{} {}:\n{}'.format(user['first_name'], user['last_name'], message)

    @telegram.ext.dispatcher.run_async
    def __call__(self, _bot, update, **kwargs):
        user = update.message.chat if update.message else update.callback_query.from_user
        chat = mongo.chats.get_active_chat_by_telegram_id(user['id'])
        if not chat:
            update.message.reply_text(
                'No active chats found. Connect to a user with {} command'.format(
                    bot.commands.connect.ConnectCommand.get_command(),
                ),
            )
            return

        result = vk.api.send_message(
            chat['vk_id'],
            self._format_message(user, update.message.text),
        )

        result = json.loads(result.text)
        if result.get('error'):
            update.message.reply_text('Sorry. Error happened. The incident is already reported')
            bot_logger.error(result)
            return False

        return True

    def __str__(self):
        return '{}'.format(self._PATTERN)
