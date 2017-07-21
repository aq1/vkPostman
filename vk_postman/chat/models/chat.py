from django.db import models
from vk_postman.chat.models import VkUser, TelegramUser


class Chat(models.Model):

    vk_user = models.ForeignKey(VkUser)
    TelegramUser = models.ForeignKey(TelegramUser)
