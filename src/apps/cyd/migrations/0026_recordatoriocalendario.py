# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2020-05-04 14:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cyd', '0025_auto_20200326_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordatorioCalendario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('observacion', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('capacitador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordatorios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Recordatorio',
                'verbose_name_plural': 'Recordatorios',
            },
        ),
    ]
