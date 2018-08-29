import vk
import mongo
from bot.commands import BaseCommand


class ConnectCommand(BaseCommand):

    _COMMAND = 'connect'
    _DESCRIPTION = 'Start a chat with user.'
    _connected = 'You are now chatting with {vk_user[first_name]} {vk_user[last_name]}'
    _user_is_busy = (
        'Sorry! User you are trying to connect '
        'is already connected to another telegram user. Try later.'
    )
    _already_connected = 'You are already connected to this user.'

    def _call(self, user, _bot, update, **kwargs):
        """
        First, check if vk user is free to chat and is not connected to another telegram user.
        Then disconnect from previous chats.
        Then connect to a new chat.
        """
        try:
            vk_id = int(kwargs['args'][0])
        except (KeyError, IndexError):
            update.message.reply_text('Vk user\'s id is required')
            return
        except ValueError:
            update.message.reply_text('Parameter must be a number')
            return

        vk_user = mongo.users.get_vk_user(vk_id)
        if not vk_user:
            user = vk.get_user(vk_id)
            vk_user = mongo.users.save_vk_user(user)

        active_chat = mongo.chats.get_active_chat_by_vk_id(vk_id)
        if active_chat and active_chat['telegram_id'] != user.id:
            update.message.reply_text(self._user_is_busy)
            return
        elif active_chat:
            update.message.reply_text(self._already_connected)
            return
        else:
            mongo.chats.create_chat(vk_id, user.id)

        update.message.reply_text(self._connected.format(vk_user=vk_user))
