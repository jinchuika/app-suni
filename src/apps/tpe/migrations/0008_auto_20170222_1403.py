# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-22 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tpe', '0007_auto_20170221_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketsoporte',
            name='descripcion',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticketregistrotipo',
            name='tipo',
            field=models.CharField(max_length=30),
        ),
    ]
