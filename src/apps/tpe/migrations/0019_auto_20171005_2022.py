# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-05 20:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tpe', '0018_auto_20170809_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluacionMonitoreo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('punteo', models.PositiveSmallIntegerField()),
                ('monitoreo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='tpe.Monitoreo')),
            ],
            options={
                'verbose_name': 'Evaluación de monitoreo',
                'verbose_name_plural': 'Evaluaciones de monitoreo',
            },
        ),
        migrations.CreateModel(
            name='EvaluacionPregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.TextField()),
                ('activa', models.BooleanField(default=True)),
                ('minimo', models.PositiveIntegerField(default=1)),
                ('maximo', models.PositiveIntegerField(default=5)),
            ],
            options={
                'verbose_name': 'Pregunta de evaluación',
                'verbose_name_plural': 'Preguntas de evaluación',
            },
        ),
        migrations.AddField(
            model_name='evaluacionmonitoreo',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpe.EvaluacionPregunta'),
        ),
        migrations.AlterUniqueTogether(
            name='evaluacionmonitoreo',
            unique_together=set([('monitoreo', 'pregunta')]),
        ),
    ]