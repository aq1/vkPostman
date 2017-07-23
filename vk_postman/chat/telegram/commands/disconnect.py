from chat.models import TelegramUser, VkUser, Chat

from chat.telegram.commands import CommandBase


class Disconnect(CommandBase):

    _description = 'Close currently active chat.'
    _SUCCESS_MSG = 'You are exited chat with {vk_user}'

    @classmethod
    def _execute(cls, telegram_user_id, *args):
        vk_user_id = args[0]
        telegram_user, _ = TelegramUser.objects.get_or_create(id=telegram_user_id)
        vk_user, _ = VkUser.objects.get_or_create(id=vk_user_id)

        Chat.objects.filter(
            telegram_user=telegram_user,
            vk_user=vk_user,
        ).update(is_active=False)
