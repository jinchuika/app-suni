# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-02-13 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0041_entrada_fecha_cierre'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradadetalle',
            name='fecha_dispositivo',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entradadetalle',
            name='fecha_repuesto',
            field=models.DateField(blank=True, null=True),
        ),
    ]