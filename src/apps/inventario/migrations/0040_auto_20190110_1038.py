# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-01-10 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0039_auto_20190108_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='ram',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]