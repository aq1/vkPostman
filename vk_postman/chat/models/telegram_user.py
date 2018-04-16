from django.db import models


class TelegramUser(models.Model):

    first_name = models.CharField(max_length=255, default='', blank=True)
    last_name = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return '{} {} {}'.format(self.first_name, self.last_name, self.id)
