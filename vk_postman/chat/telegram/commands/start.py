from chat.telegram.commands import CommandBase


class Start(CommandBase):

    _description = 'Start working with the bot.'
    _SUCCESS_MSG = (
        'Hey! I am VkPostman Bot.\n'
        'I will create a chat between you and vk user.\n'
        'Type /help to see available commands.\n'
    )
