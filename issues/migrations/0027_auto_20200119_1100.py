# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-01-19 11:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0026_auto_20200112_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='voters',
            field=models.ManyToManyField(default=0, to=settings.AUTH_USER_MODEL),
        ),
    ]
