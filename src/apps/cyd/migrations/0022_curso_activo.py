# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2020-01-23 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyd', '0021_grupo_activo'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='activo',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
    ]