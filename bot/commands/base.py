import telegram.ext

import mongo
import bot


class BaseCommand(telegram.ext.CommandHandler):

    _COMMAND = ''
    _RETURN_STATE = bot.states.START

    _SUCCESS_MESSAGE = ''

    _DESCRIPTION = ''

    def __init__(self,
                 command=None,
                 callback=None,
                 filters=None,
                 allow_edited=False,
                 pass_args=False,
                 pass_update_queue=False,
                 pass_job_queue=False,
                 pass_user_data=False,
                 pass_chat_data=False):

        command = command or self._COMMAND
        callback = callback or self.__call__

        if not command:
            raise ValueError('Expected `command` argument')

        super().__init__(command,
                         callback,
                         filters,
                         allow_edited,
                         pass_args,
                         pass_update_queue,
                         pass_job_queue,
                         pass_user_data,
                         pass_chat_data)

    def _call(self, bot, update, **kwargs):
        """
        Return bool indicating successful execution
        """
        return True

    @telegram.ext.dispatcher.run_async
    def __call__(self, bot, update, **kwargs):
        mongo.users.save_telegram_user(update.message.chat)

        ok = self._call(bot, update, **kwargs)

        if ok and self._SUCCESS_MESSAGE:
            update.message.reply_text(self._SUCCESS_MESSAGE)

        return self._RETURN_STATE

    def __str__(self):
        return '{} - {}'.format(self._COMMAND, self._DESCRIPTION)
