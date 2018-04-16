from django.contrib import admin

from chat.models import *


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = '__str__', 'is_active', 'vk_user', 'telegram_user', 'telegram_active', 'vk_active'


@admin.register(VkUser)
class VkUserAdmin(admin.ModelAdmin):
    pass


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass
