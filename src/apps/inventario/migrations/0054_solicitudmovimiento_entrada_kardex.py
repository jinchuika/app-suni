# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-05 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kardex', '0016_auto_20190304_1429'),
        ('inventario', '0053_solicitudmovimiento_salida_kardex'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudmovimiento',
            name='entrada_kardex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entrada_kardex', to='kardex.Entrada'),
        ),
    ]
