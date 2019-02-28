from bot.commands import (
    BaseCommand,
    ConnectCommand,
    HelpCommand,
    MessageToAdminCommand,
)


class StartCommand(BaseCommand):

    _COMMAND = 'start'
    _DESCRIPTION = 'Start working with the bot.'
    _SUCCESS_MESSAGE = (
        'Hello! I am VkPostman Bot.\n'
        'I will create a chat between you and vk user.\n'
        'Before sending a message to a vk user, you must connect to him (create a chat).\n'
        'Type {} "vk_user_id" to connect.\n'
        'You can text admins with\n'
        '{} {{Your message here}} command.\n\n'
        '{} for list of commands'
    ).format(
        ConnectCommand.get_command(),
        MessageToAdminCommand.get_command(),
        HelpCommand.get_command(),
    )
