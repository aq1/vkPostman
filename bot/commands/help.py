from bot.commands import BaseCommand, MessageToAdminCommand


class HelpCommand(BaseCommand):

    _COMMAND = 'help'
    _DESCRIPTION = 'Basic help.'
    _SUCCESS_MESSAGE = (
        'Okay, let\'s start.\n'
        'Before sending a message to a vk user, you must connect to him (create a chat).\n'
        'Type /connect "vk_user_id" to connect!\n'
        'You can write to admins with\n'
        '{} {{Your message here}} command.'
    ).format(MessageToAdminCommand.get_command())
