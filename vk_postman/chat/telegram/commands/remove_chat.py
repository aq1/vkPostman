from chat.models import TelegramUser, VkUser, Chat

from chat.telegram.commands import CommandBase


class RemoveChat(CommandBase):

    _description = 'Remove chat from history.'
    _SUCCESS_MSG = 'Chat with {vk_user} has been removed'

    @classmethod
    def _execute(cls, from_, args):
        telegram_user, _ = TelegramUser.objects.get_or_create(id=from_['id'])

        try:
            vk_user_id = int(args[0])
        except IndexError:
            return cls._execution_result(False, 'Vk user\'s id is required')
        except ValueError:
            return cls._execution_result(False, 'Paramter must be a number')

        try:
            chat = Chat.objects.get(
                telegram_user=telegram_user,
                vk_user_id=vk_user_id,
            )
        except Chat.DoesNotExist:
            return cls._execution_result(True, 'You are not connected to any vk user')

        chat.delete()

        return cls._execution_result(True, cls._SUCCESS_MSG.format(vk_user=cls._get_vk_user_url(chat.vk_user_id)))
