# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-01-29 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_subscriber_card_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
