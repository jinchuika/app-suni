# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-21 15:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0004_escpoblacion'),
        ('mye', '0008_auto_20170321_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='validacion',
            name='alumna',
        ),
        migrations.RemoveField(
            model_name='validacion',
            name='alumno',
        ),
        migrations.RemoveField(
            model_name='validacion',
            name='maestra',
        ),
        migrations.RemoveField(
            model_name='validacion',
            name='maestro',
        ),
        migrations.RemoveField(
            model_name='validacion',
            name='total_alumno',
        ),
        migrations.RemoveField(
            model_name='validacion',
            name='total_maestro',
        ),
        migrations.AddField(
            model_name='validacion',
            name='poblacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='validaciones', to='escuela.EscPoblacion'),
        ),
    ]