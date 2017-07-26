from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


class VkUser(models.Model):

    first_name = models.CharField(max_length=255, default='', blank=True)
    last_name = models.CharField(max_length=255, default='', blank=True)


@receiver(pre_save, sender=VkUser)
def fetch_vk_user_data(instance, **kwargs):
    if instance.first_name or instance.last_name:
        return

    from chat.vk import vk_api
    r = vk_api.call('get', 'users.get', params={'user_ids': instance.id})

    try:
        user_info = r.json()['response'][0]
    except (ValueError, IndexError):
        return

    instance.first_name = user_info['first_name']
    instance.last_name = user_info['last_name']
