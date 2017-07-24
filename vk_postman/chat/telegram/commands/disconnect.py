from chat.models import TelegramUser, VkUser, Chat

from chat.telegram.commands import CommandBase


class Disconnect(CommandBase):

    _description = 'Close currently active chat.'
    _SUCCESS_MSG = 'You have exited chat with {vk_user}'

    @classmethod
    def _execute(cls, telegram_user_id, *args):
        telegram_user, _ = TelegramUser.objects.get_or_create(id=telegram_user_id)

        try:
            chat = Chat.objects.get(
                telegram_user=telegram_user,
                telegram_active=True,
                vk_active=True,
            )
        except Chat.DoesNotExist:
            return True, 'You are not connected to any vk user'
        except Chat.MultipleObjectsReturned:
            Chat.objects.filter(telegram_user=telegram_user_id).update(
                telegram_active=False,
                vk_active=False,
            )
            return True, 'Disconnected from all chats.'

        chat.telegram_active = False
        chat.vk_active = False
        chat.save()

        return True, cls._SUCCESS_MSG.format(vk_user=cls._get_vk_user_url(chat.vk_user_id))
