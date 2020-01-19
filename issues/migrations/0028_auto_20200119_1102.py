# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-01-19 11:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0027_auto_20200119_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='voters',
            field=models.ManyToManyField(default='', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
