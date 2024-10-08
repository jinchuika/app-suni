# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2023-01-27 21:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beqt', '0003_cargadorlaptopbeqt_dispositivoredbeqt_regletabeqt_upsbeqt'),
    ]

    operations = [
        migrations.CreateModel(
            name='CargadorTabletBeqt',
            fields=[
                ('dispositivobeqt_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='beqt.DispositivoBeqt')),
                ('indice', models.PositiveIntegerField(editable=False, unique=True)),
                ('alimentacion', models.CharField(blank=True, max_length=80, null=True, verbose_name='Alimentacion')),
                ('salida', models.CharField(blank=True, max_length=80, null=True, verbose_name='Salida voltaje')),
            ],
            options={
                'ordering': ['indice'],
                'verbose_name': 'Cargador Tablet',
                'verbose_name_plural': 'Cargadores Tablets',
                'db_table': 'dispositivo_cargador_tablet_beqt',
            },
            bases=('beqt.dispositivobeqt',),
        ),
        migrations.CreateModel(
            name='CaseTabletBeqt',
            fields=[
                ('dispositivobeqt_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='beqt.DispositivoBeqt')),
                ('indice', models.PositiveIntegerField(editable=False, unique=True)),
                ('compatibilidad', models.CharField(blank=True, max_length=80, null=True, verbose_name='Compatibilidad')),
                ('color', models.CharField(blank=True, max_length=80, null=True, verbose_name='Color')),
                ('estilo', models.CharField(blank=True, max_length=80, null=True, verbose_name='Estilo')),
                ('material', models.CharField(blank=True, max_length=80, null=True, verbose_name='Material')),
                ('dimensiones', models.CharField(blank=True, max_length=80, null=True, verbose_name='Dimensiones')),
            ],
            options={
                'ordering': ['indice'],
                'verbose_name': 'Case Tablet',
                'verbose_name_plural': 'Cases Tablets',
                'db_table': 'dispositivo_case_tablet_beqt',
            },
            bases=('beqt.dispositivobeqt',),
        ),
        migrations.AddIndex(
            model_name='casetabletbeqt',
            index=models.Index(fields=['indice'], name='dispositivo_indice_593665_idx'),
        ),
        migrations.AddIndex(
            model_name='cargadortabletbeqt',
            index=models.Index(fields=['indice'], name='dispositivo_indice_2a7d07_idx'),
        ),
        migrations.AddField(
            model_name='tabletbeqt',
            name='cargador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cargador_tablets_beqt', to='beqt.CargadorTabletBeqt', verbose_name='Cargador'),
        ),
        migrations.AddField(
            model_name='tabletbeqt',
            name='estuche',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='case_tablets_beqt', to='beqt.CaseTabletBeqt', verbose_name='Case'),
        ),
    ]
