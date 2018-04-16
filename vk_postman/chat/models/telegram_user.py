from django.db import models


class TelegramUser(models.Model):

    first_name = models.CharField(max_length=255, default='', blank=True)
    last_name = models.CharField(max_length=255, default='', blank=True)

    def __unicode__(self):
        return '{} {}'.format(self.last_name, self.first_name)
