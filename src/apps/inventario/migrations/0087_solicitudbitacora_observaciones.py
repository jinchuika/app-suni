# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2023-06-14 03:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0086_auto_20230607_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudbitacora',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
    ]
