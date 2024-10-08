# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2021-10-17 15:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('controlNotas', '0002_auto_20201016_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='cn_evaluacion_creado_por',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.CASCADE, related_name='cn_evaluacion_creado_por', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grado',
            name='cn_grado_creado_por',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.CASCADE, related_name='cn_grado_creado_por', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='materia',
            name='materia_creado_por',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notas',
            name='cn_notas_creado_por',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='semestre',
            name='cn_semestre_creado_por',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
