import mongo
from bot.commands import BaseCommand


class RemoveChat(BaseCommand):

    _COMMAND = 'remove_chat'
    _SUCCESS_MESSAGE = 'Chat has been removed'
    _DESCRIPTION = 'Remove chat from history.'

    def _call(self, user, _bot, update, **kwargs):
        """
        Return bool indicating successful execution
        """
        try:
            vk_id = int(kwargs['args'][0])
        except (KeyError, IndexError):
            update.message.reply_text('Vk user\'s id is required')
            return
        except ValueError:
            update.message.reply_text('Parameter must be a number')
            return

        chat = mongo.chats.get_chat(vk_id, user['id'])
        if not chat:
            update.message.reply_text('No chat found')
            return

        mongo.chats.delete_chat(chat['_id'])
        return True
