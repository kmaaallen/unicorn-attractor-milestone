# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-12-27 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0015_auto_20191227_1329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issue',
            options={'ordering': ('-priority', '-votes')},
        ),
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default='LOW', max_length=6),
        ),
    ]