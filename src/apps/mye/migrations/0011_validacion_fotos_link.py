# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-23 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mye', '0010_auto_20170321_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='validacion',
            name='fotos_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
