from chat.telegram.commands import CommandBase


class Start(CommandBase):

    _SUCCESS_MSG = '''
        Hey! I am VkPostman Bot.
        I will create a chat between you and vk user.
        Type /help to see available commands.
    '''.strip()
