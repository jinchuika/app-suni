# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-16 17:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170908_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('color', models.CharField(choices=[('#0073b7', 'azul'), ('#39cccc', 'aqua'), ('green', 'verde'), ('#f3c612', 'amarillo'), ('#dd4b39', 'rojo'), ('#605ca8', 'morado'), ('#f012be', 'rosa'), ('#ff851b', 'gris'), ('#777777', 'naranja')], default='#0073b7', max_length=20)),
            ],
            options={
                'verbose_name': 'Organización',
                'verbose_name_plural': 'Organizaciones',
            },
        ),
        migrations.RemoveField(
            model_name='perfiltelefono',
            name='perfil',
        ),
        migrations.DeleteModel(
            name='PerfilTelefono',
        ),
        migrations.AddField(
            model_name='perfil',
            name='organizacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.Organizacion', verbose_name='Organización'),
        ),
    ]