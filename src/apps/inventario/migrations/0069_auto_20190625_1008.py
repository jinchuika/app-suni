# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-06-25 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0068_accionbitacora_solicitudbitacora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accionbitacora',
            name='estado',
            field=models.CharField(max_length=100),
        ),
    ]
