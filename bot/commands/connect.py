import mongo
from bot.commands import BaseCommand


class ConnectCommand(BaseCommand):

    _COMMAND = 'connect'
    _DESCRIPTION = 'Start a chat with user.'
    _SUCCESS_MESSAGE = 'You are now chatting with {vk_user}'
    _USER_IS_BUSY = 'Sorry! User you are trying to connect is already connected to another telegram user. Try later.'

    def _call(self, bot, update, **kwargs):
        """
        First, check if vk user is free to chat and is not connected to another telegram user.
        Then disconnect from previous chats.
        Then connect to a new chat.
        """
        try:
            vk_id = int(kwargs['args'])
        except KeyError:
            update.message.reply_text('Vk user\'s id is required')
            return
        except ValueError:
            update.message.reply_text('Paramter must be a number')
            return

        telegram_user = mongo.get_telegram_user(update.message.chat.id)
        vk_user = mongo.get_vk_user(vk_id)

        chat = mongo.get_chat(update.message.chat.id, vk_id)

        if Chat.objects.filter(
            vk_user=vk_user,
            telegram_active=True,
            vk_active=True,
        ).exclude(telegram_user=telegram_user).exists():
            return cls._execution_result(False, cls._USER_IS_BUSY)

        Chat.objects.filter(
            telegram_user=telegram_user,
        ).update(telegram_active=False, vk_active=False)

        chat, created = Chat.objects.get_or_create(
            telegram_user=telegram_user,
            vk_user=vk_user,
        )

        if not created and not (chat.telegram_active and chat.vk_active):
            chat.telegram_active = True
            chat.vk_active = True
            chat.save()

        return cls._execution_result(True)
