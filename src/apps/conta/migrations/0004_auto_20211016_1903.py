# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2021-10-17 01:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conta', '0003_precioestandar_revaluar'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientodispositivo',
            name='creado_por',
            field=models.ForeignKey(blank=True, default=49, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movimientorepuesto',
            name='creado_por',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='periodofiscal',
            name='creado_por',
            field=models.ForeignKey(blank=True, default=49, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='preciodispositivo',
            name='creado_por',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='preciorepuesto',
            name='creado_por',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='precioestandar',
            name='creado_por',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
