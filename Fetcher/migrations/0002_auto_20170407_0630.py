# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 06:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fetcher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 7, 6, 30, 31, 502173)),
        ),
    ]
