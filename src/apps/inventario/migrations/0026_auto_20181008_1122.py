# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-10-08 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0025_auto_20181005_0927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paquete',
            name='dispositivos',
        ),
        migrations.AddField(
            model_name='salidainventario',
            name='entrada',
            field=models.ManyToManyField(blank=True, related_name='tipo_entrada', to='inventario.Entrada'),
        ),
    ]
