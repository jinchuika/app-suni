# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-07-18 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kardex', '0016_auto_20190304_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradadetalle',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True),
        ),
    ]