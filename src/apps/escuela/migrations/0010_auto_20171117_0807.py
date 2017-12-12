# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-11-17 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0009_auto_20171026_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='EscMatricula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.PositiveIntegerField(verbose_name='Año')),
                ('m_promovido', models.PositiveIntegerField(default=0, verbose_name='Mujeres promovidas')),
                ('m_no_promovido', models.PositiveIntegerField(default=0, verbose_name='Mujeres no promovidas')),
                ('m_retirado', models.PositiveIntegerField(default=0, verbose_name='Mujeres retiradas')),
                ('h_promovido', models.PositiveIntegerField(default=0, verbose_name='Hombres promovidos')),
                ('h_no_promovido', models.PositiveIntegerField(default=0, verbose_name='Hombres no promovidos')),
                ('h_retirado', models.PositiveIntegerField(default=0, verbose_name='Hombres retirados')),
                ('escuela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matriculas', to='escuela.Escuela')),
            ],
            options={
                'ordering': ['escuela', '-ano'],
                'verbose_name_plural': 'Matrículas de escuelas',
                'verbose_name': 'Matrícula de escuela',
            },
        ),
        migrations.CreateModel(
            name='EscRendimientoAcademico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.PositiveIntegerField(verbose_name='Año')),
                ('insatisfactorio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('debe_mejorar', models.DecimalField(decimal_places=2, max_digits=5)),
                ('satisfactorio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('excelente', models.DecimalField(decimal_places=2, max_digits=5)),
                ('no_evaluado', models.DecimalField(decimal_places=2, max_digits=5)),
                ('escuela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rendimientos', to='escuela.Escuela')),
            ],
            options={
                'ordering': ['escuela', '-ano'],
                'verbose_name_plural': 'Rendimientos académicos',
                'verbose_name': 'Rendimiento académico',
            },
        ),
        migrations.CreateModel(
            name='EscRendimientoMateria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materia', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Materias de rendimiento',
                'verbose_name': 'Materia de rendimiento',
            },
        ),
        migrations.AddField(
            model_name='escrendimientoacademico',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros', to='escuela.EscRendimientoMateria'),
        ),
    ]