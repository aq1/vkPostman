# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 08:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_chat_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='vkuser',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='vkuser',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
