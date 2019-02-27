import telegram.ext

from utils.logging import bot_logger
import mongo
import bot


class BaseCommand(telegram.ext.CommandHandler):

    _COMMAND = ''
    _RETURN_STATE = bot.states.START

    _COMMAND_FAILED_MESSAGE = 'Sorry. Something went wrong. We are investigating.'
    _SUCCESS_MESSAGE = ''

    _DESCRIPTION = ''

    def __init__(
            self,
            command=None,
            callback=None,
            filters=None,
            allow_edited=False,
            pass_args=False,
            pass_update_queue=False,
            pass_job_queue=False,
            pass_user_data=False,
            pass_chat_data=False
    ):

        command = command or self._COMMAND
        callback = callback or self.__call__

        if not command:
            raise ValueError('Expected `command` argument')

        super().__init__(
            command,
            callback,
            filters,
            allow_edited,
            pass_args,
            pass_update_queue,
            pass_job_queue,
            pass_user_data,
            pass_chat_data,
        )

    @classmethod
    def get_command(cls):
        return '/{}'.format(cls._COMMAND)

    def _call(self, user, _bot, update, **kwargs):
        """
        Return bool indicating successful execution
        """
        return True

    def _callback(self, user, _bot, update, **kwargs):
        return True

    @telegram.ext.dispatcher.run_async
    def __call__(self, _bot, update, **kwargs):
        user = update.message.chat if update.message else update.callback_query.from_user
        mongo.users.save_telegram_user(user)

        try:
            if update.message:
                ok = self._call(user, _bot, update, **kwargs)
            else:
                ok = self._callback(user, _bot, update, **kwargs)
        except:
            bot_logger.exception('bot')
            _bot.send_message(
                chat_id=user.id,
                text=self._COMMAND_FAILED_MESSAGE,
            )
            return

        if ok and self._SUCCESS_MESSAGE:
            if update.message:
                update.message.reply_text(self._SUCCESS_MESSAGE)
            else:
                _bot.send_message(
                    chat_id=user.id,
                    text=self._SUCCESS_MESSAGE,
                )

        return self._RETURN_STATE

    def __str__(self):
        return '{} - {}'.format(self._COMMAND, self._DESCRIPTION)
