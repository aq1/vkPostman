import settings

from bot.commands import BaseCommand


class MessageToAdminCommand(BaseCommand):

    _COMMAND = 'message_to_admin'
    _DESCRIPTION = 'Write to admin.'
    _SUCCESS_MESSAGE = 'Message sent'

    @staticmethod
    def _format_message(user, message):
        return 'Message from user "{} {} ({})" to admin.\n\n{}'.format(
            user['first_name'],
            user['last_name'],
            user['id'],
            message,
        )

    def _call(self, user, _bot, update, **kwargs):
        if not kwargs['args']:
            update.message.reply_text('Message is required.')
            return

        message = self._format_message(user, ' '.join(kwargs['args']))
        _bot.sendMessage(settings.ADMIN_ID, message)
        return True
