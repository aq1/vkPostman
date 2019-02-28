from bot.commands import BaseCommand


class HelpCommand(BaseCommand):

    _COMMAND = 'help'
    _DESCRIPTION = 'Basic help.'

    def _call(self, user, _bot, update, **kwargs):
        from bot.main import commands
        update.message.reply_text('\n'.join([
            '/{}'.format(command)
            for command in commands
        ]))
        return True
