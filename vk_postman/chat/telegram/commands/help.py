from chat.telegram.commands import CommandBase


class Help(CommandBase):

    _description = 'Basic help.'
    _SUCCESS_MSG = '''
        Okay, let's start.
        Before send a message to a vk user, you must connect to him (create a chat).
        Type /connect {vk_user_id} to connect!
    '''.strip()
