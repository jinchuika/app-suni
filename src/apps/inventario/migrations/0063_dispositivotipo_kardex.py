# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-15 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0062_merge_20190312_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispositivotipo',
            name='kardex',
            field=models.BooleanField(default=False),
        ),
    ]
