from chat.models import TelegramUser, VkUser, Chat

from chat.telegram.commands import CommandBase


class Connect(CommandBase):

    _description = 'Start a chat with user.'
    _SUCCESS_MSG = 'You are now chatting with {vk_user}'

    @classmethod
    def _execute(cls, telegram_user_id, *args):
        """
        First, disconnect from previous chats.
        Then connect to a new chat.
        """
        vk_user_id = args[0]
        telegram_user, _ = TelegramUser.objects.get_or_create(id=telegram_user_id)
        vk_user, _ = VkUser.objects.get_or_create(id=vk_user_id)

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
