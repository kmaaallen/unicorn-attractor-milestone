# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-03-29 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_ticket_resolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='resolution',
            field=models.TextField(max_length=600),
        ),
    ]