# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-01-11 21:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='escuelasede',
            options={'managed': False, 'verbose_name': 'Escuela capacitada', 'verbose_name_plural': 'Escuelas capacitadas'},
        ),
    ]
