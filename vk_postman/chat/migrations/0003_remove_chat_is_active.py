# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 17:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20170724_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='is_active',
        ),
    ]