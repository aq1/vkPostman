from django.db import models
from chat.models import VkUser, TelegramUser


class Chat(models.Model):

    vk_user = models.ForeignKey(VkUser)
    telegram_user = models.ForeignKey(TelegramUser)
    is_active = models.BooleanField(default=True, blank=True)
    telegram_active = models.BooleanField(default=True, blank=True)
    vk_active = models.BooleanField(default=True, blank=True)
