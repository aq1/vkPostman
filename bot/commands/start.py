from bot.commands import BaseCommand


class StartCommand(BaseCommand):

    _COMMAND = 'start'
    _DESCRIPTION = 'Start working with the bot.'
    _SUCCESS_MESSAGE = (
        'Hello! I am VkPostman Bot.\n'
        'I will create a chat between you and vk user.\n'
        'Type /help to see available commands.\n'
    )
