# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-04 20:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kardex', '0016_auto_20190304_1429'),
        ('inventario', '0052_solicitudmovimiento_rechazar'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudmovimiento',
            name='salida_kardex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salida_kardex', to='kardex.Salida'),
        ),
    ]