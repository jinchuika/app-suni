# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-07-12 13:30
from __future__ import unicode_literals

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0073_desechosalida_comprobante'),
    ]

    operations = [
        migrations.AddField(
            model_name='desechosalida',
            name='codigo_qr',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='qr_desecho'),
        ),
    ]
