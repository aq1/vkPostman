from chat.models import TelegramUser, VkUser, Chat

from chat.telegram.commands import CommandBase


class Connect(CommandBase):

    _description = 'Start a chat with user.'
    _SUCCESS_MSG = 'You are now chatting with {vk_user}'
    _USER_IS_BUSY = 'Sorry! User you are trying to connect is already connected to another telegram user. Try later.'

    @classmethod
    def _execute(cls, from_, args):
        """
        First, check if vk user is free to chat and is not connected to another telegram user.
        Then disconnect from previous chats.
        Then connect to a new chat.
        """
        try:
            vk_user_id = args[0]
        except IndexError:
            return False, 'Vk user\'s id is required'

        telegram_user, tg_user_created = TelegramUser.objects.get_or_create(
            id=from_['id'],
            defaults={
                'last_name': from_['last_name'],
                'first_name': from_['first_name'],
            }
        )
        vk_user, _ = VkUser.objects.get_or_create(id=vk_user_id)

        if Chat.objects.filter(
            vk_user=vk_user,
            telegram_active=True,
            vk_active=True,
        ).exclude(telegram_user=telegram_user).exists():
            return False, cls._USER_IS_BUSY

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

        return True, None
