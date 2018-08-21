import settings

from bot.commands import BaseCommand


class MessageToAdminCommand(BaseCommand):

    _COMMAND = 'message_to_admin'
    _DESCRIPTION = 'Write to admin.'
    _SUCCESS_MESSAGE = 'Message sent'

    @staticmethod
    def _format_message(from_, message):
        return 'Message from user "{} {} ({})" to admin.\n\n{}'.format(
            from_['first_name'],
            from_['last_name'],
            from_['id'],
            message,
        )

    def _call(self, bot, update, **kwargs):
        if not kwargs['args']:
            update.message.reply_text('Message is required.')
            return

        message = self._format_message(update.message.chat, ' '.join(kwargs['args']))
        bot.sendMessage(settings.ADMIN_ID, message)
        return True
