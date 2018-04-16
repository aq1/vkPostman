from django.contrib import admin

from chat.models import *


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = 'vk_user', 'telegram_user', 'telegram_active', 'vk_active'
