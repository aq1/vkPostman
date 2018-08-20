from bot.commands import BaseCommand


class HelpCommand(BaseCommand):

    _COMMAND = 'help'
    _DESCRIPTION = 'Basic help.'
    _SUCCESS_MESSAGE = (
        'Okay, let\'s start.\n'
        'Before sending a message to a vk user, you must connect to him (create a chat).\n'
        'Type /connect "vk_user_id" to connect!\n'
        'You can write to admins with /write_to_admin &lt;Your message here&gt; command.'
    )
