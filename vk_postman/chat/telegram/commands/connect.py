from chat.models import TelegramUser, VkUser, Chat

from chat.telegram.commands import CommandBase


class Connect(CommandBase):

    _description = 'Start a chat with user.'
    _SUCCESS_MSG = 'You are now chatting with {vk_user}'
    _USER_IS_BUSY = 'Sorry! User you are trying to connect is already connected to another telegram user. Try later.'
    _USER_IS_BUSY = 'Sorry! User you are trying to connect is already connected to another telegram user. Try later.'

    @classmethod
    def _execute(cls, telegram_user_id, *args):
        """
        First, check if vk user is free to chat and is not connected to another telegram user.
        Then disconnect from previous chats.
        Then connect to a new chat.
        """
        vk_user_id = args[0]
        telegram_user, _ = TelegramUser.objects.get_or_create(id=telegram_user_id)
        vk_user, _ = VkUser.objects.get_or_create(id=vk_user_id)

        if Chat.objects.filter(
            vk_user=vk_user,
            is_active=True
        ).exclude(telegram_user=telegram_user).exist():
            return False, cls._USER_IS_BUSY

        Chat.objects.filter(
            telegram_user=telegram_user,
            vk_user=vk_user,
        ).update(is_active=False)

        chat, created = Chat.objects.get_or_create(
            telegram_user=telegram_user,
            vk_user=vk_user,
        )

        if not (created or chat.is_active):
            chat.is_active = True
            chat.save()

        return True, None
