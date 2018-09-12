from django.db import models
from chat.models import VkUser, TelegramUser


class Chat(models.Model):

    vk_user = models.ForeignKey(VkUser, on_delete=models.CASCADE)
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    telegram_active = models.BooleanField(default=True, blank=True)
    vk_active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return 'Chat {}'.format(self.id)

    def is_active(self):
        return self.telegram_active and self.vk_active

    @classmethod
    def disconnect(cls, ids=None):
        chats = cls.objects.all()
        if ids:
            chats = chats.filter(id__in=ids)
        return chats.update(vk_active=False, telegram_active=False)
