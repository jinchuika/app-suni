# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-02-13 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0040_auto_20190110_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='fecha_cierre',
            field=models.DateField(blank=True, null=True),
        ),
    ]
