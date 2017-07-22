from chat.models import TelegramUser, VkUser, Chat

from chat.telegram.commands import CommandBase


class Connect(CommandBase):

    _SUCCESS_MSG = 'You are now chatting with {}'

    @staticmethod
    def _get_vk_user_url(vk_user_id):
        return 'https://vk.com/id{}'.format(vk_user_id)

    @classmethod
    def execute(cls, telegram_user_id, *args):
        vk_user_id = args[0]
        telegram_user, _ = TelegramUser.objects.get_or_create(id=telegram_user_id)
        vk_user, _ = VkUser.objects.get_or_create(id=vk_user_id)
        chat, created = Chat.objects.get_or_create(
            telegram_user=telegram_user,
            vk_user=vk_user,
        )

        if not (created or chat.is_active):
            chat.is_active = True
            chat.save()

        cls.send_message(telegram_user_id, cls._SUCCESS_MSG.format(cls._get_vk_user_url(args[0])))
