# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2020-08-06 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bienestar', '0004_auto_20200806_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaborador',
            name='email',
            field=models.CharField(default='', max_length=150, verbose_name='Correo Electronico'),
            preserve_default=False,
        ),
    ]
