# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2020-05-04 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kardex', '0017_auto_20190718_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='factura',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
