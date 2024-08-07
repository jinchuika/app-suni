# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2023-01-11 03:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import easy_thumbnails.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0084_auto_20230110_2101'),
        ('crm', '0005_auto_20211017_0942'),
        ('tpe', '0022_auto_20211017_1045'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mye', '0015_auto_20211017_1040'),
        ('escuela', '0011_auto_20211017_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionTecnico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipos', models.ManyToManyField(blank=True, related_name='tipos_disponibles_beqt', to='inventario.DispositivoTipo')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tipos_dispositivos_beqt', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Asignacion de técnico',
                'verbose_name_plural': 'Asignaciones de técnicos',
            },
        ),
        migrations.CreateModel(
            name='CambioEstadoBeqt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('creado_por', models.ForeignKey(default=49, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cambio de estado',
                'verbose_name_plural': 'Cambios de estado',
            },
        ),
        migrations.CreateModel(
            name='CambioEtapaBeqt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechahora', models.DateTimeField(default=django.utils.timezone.now)),
                ('creado_por', models.ForeignKey(default=49, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cambio de etapa',
                'verbose_name_plural': 'Cambios de etapa',
            },
        ),
        migrations.CreateModel(
            name='DispositivoBeqt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('triage', models.SlugField(blank=True, editable=False, unique=True)),
                ('impreso', models.BooleanField(default=False, verbose_name='Impreso')),
                ('modelo', models.CharField(blank=True, max_length=80, null=True)),
                ('serie', models.CharField(blank=True, max_length=80, null=True)),
                ('codigo_qr', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='qr_dispositivo_beqt')),
                ('valido', models.BooleanField(default=True, verbose_name='Válido')),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Dispositivo',
                'verbose_name_plural': 'Dispositivos',
            },
        ),
        migrations.CreateModel(
            name='DispositivoFalla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_falla', models.TextField(verbose_name='Descripción de la falla')),
                ('descripcion_solucion', models.TextField(blank=True, null=True, verbose_name='Descripción de la solución')),
                ('fecha_inicio', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de inicio')),
                ('fecha_fin', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de fin')),
                ('terminada', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'DispositivoFalla',
                'verbose_name_plural': 'DispositivoFallas',
            },
        ),
        migrations.CreateModel(
            name='DispositivoPaquete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_aprobacion', models.DateTimeField(blank=True, null=True)),
                ('aprobado', models.BooleanField(default=False)),
                ('aprobado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='paquetes_aprobados_beqt', to=settings.AUTH_USER_MODEL)),
                ('asignado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='paquetes_asignados_beqt', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Asignación Dispositivo - Paquete',
                'verbose_name_plural': 'Asignaciones Dispositivo - Paquete',
            },
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('fecha_cierre', models.DateField(blank=True, null=True)),
                ('en_creacion', models.BooleanField(default=True)),
                ('factura', models.PositiveIntegerField(default=0)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('creada_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entradas_creadas_beqt', to=settings.AUTH_USER_MODEL)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entradas_beqt_proveedor', to='crm.Donante')),
                ('recibida_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entradas_recibidas_beqt', to=settings.AUTH_USER_MODEL)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entradas_beqt', to='inventario.EntradaTipo')),
            ],
            options={
                'verbose_name': 'Entrada',
                'verbose_name_plural': 'Entradas',
            },
        ),
        migrations.CreateModel(
            name='EntradaDetalleBeqt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField()),
                ('descripcion', models.CharField(max_length=50)),
                ('dispositivos_creados', models.BooleanField(default=False, verbose_name='Dispositivos creados')),
                ('qr_dispositivo', models.BooleanField(default=False, verbose_name='Imprimir Qr Dispositivo')),
                ('impreso', models.BooleanField(default=False, verbose_name='Impreso')),
                ('pendiente_autorizar', models.BooleanField(default=False, verbose_name='pendiente')),
                ('autorizado', models.BooleanField(default=False, verbose_name='autorizado')),
                ('fecha_dispositivo', models.DateField(blank=True, null=True)),
                ('precio_unitario', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('precio_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('creado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('entrada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles_beqt', to='beqt.Entrada')),
                ('tipo_dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalles_entrada_beqt', to='inventario.DispositivoTipo')),
            ],
            options={
                'verbose_name': 'Detalle de entrada',
                'verbose_name_plural': 'Detalles de entrada',
            },
        ),
        migrations.CreateModel(
            name='PaqueteBeqt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('indice', models.PositiveIntegerField()),
                ('cantidad', models.PositiveIntegerField(default=0)),
                ('aprobado', models.BooleanField(default=False)),
                ('aprobado_kardex', models.BooleanField(default=False)),
                ('desactivado', models.BooleanField(default=False)),
                ('creado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('entrada', models.ManyToManyField(blank=True, null=True, related_name='tipo_entrada_beqt', to='beqt.Entrada')),
            ],
            options={
                'verbose_name': 'Paquete de salida',
                'verbose_name_plural': 'Paquetes de salida',
            },
        ),
        migrations.CreateModel(
            name='PaqueteTipoBeqt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=35, verbose_name='Nombre del tipo')),
                ('creada_por', models.ForeignKey(default=49, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('tipo_dispositivo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.DispositivoTipo', verbose_name='Tipos de dispositivo')),
            ],
            options={
                'verbose_name': 'Tipo de paquete',
                'verbose_name_plural': 'Tipos de paquete',
            },
        ),
        migrations.CreateModel(
            name='RevisionComentarioBeqt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha_revision', models.DateTimeField(default=django.utils.timezone.now)),
                ('creado_por', models.ForeignKey(default=49, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comentario de revisión',
                'verbose_name_plural': 'Comentarios de revisión',
            },
        ),
        migrations.CreateModel(
            name='RevisionSalidaBeqt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_revision', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de revisión')),
                ('anotaciones', models.TextField(blank=True, null=True, verbose_name='Anotaciones generales')),
                ('aprobada', models.BooleanField(default=False)),
                ('revisado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Revisión de salida en contabilidad',
                'verbose_name_plural': 'Revisiones de salida en contabilidad',
            },
        ),
        migrations.CreateModel(
            name='SalidaComentarioBeqt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha_revision', models.DateTimeField(default=django.utils.timezone.now)),
                ('creado_por', models.ForeignKey(default=49, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comentario de revisión de salida control de calidad',
                'verbose_name_plural': 'Comentarios de revisión de salida control de calidad',
            },
        ),
        migrations.CreateModel(
            name='SalidaInventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('en_creacion', models.BooleanField(default=True, verbose_name='En creación')),
                ('entrega', models.BooleanField(default=True, verbose_name='Es entrega')),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('necesita_revision', models.BooleanField(default=True, verbose_name='Necesita revisión')),
                ('no_salida', models.CharField(blank=True, db_index=True, editable=False, max_length=10)),
                ('url', models.TextField(blank=True, null=True)),
                ('capacitada', models.BooleanField(default=False, verbose_name='Capacitada')),
                ('meses_garantia', models.BooleanField(default=False, verbose_name='6 meses de Garantia')),
                ('beneficiario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='beneficiario_beqt', to='crm.Donante')),
                ('cooperante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cooperante_beqt', to='mye.Cooperante')),
                ('creada_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='salidas_beqt', to=settings.AUTH_USER_MODEL)),
                ('escuela', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entregas_beqt', to='escuela.Escuela')),
                ('estado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='estados_beqt', to='inventario.SalidaEstado')),
                ('garantia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='garantias_beqt', to='tpe.TicketSoporte')),
                ('reasignado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reasignar_beqt', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Salida',
                'verbose_name_plural': 'Salidas',
            },
        ),
        migrations.CreateModel(
            name='SalidaTipoBeqt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('necesita_revision', models.BooleanField(default=True, verbose_name='Necesita revisión')),
                ('especial', models.BooleanField(default=False, verbose_name='especial')),
                ('equipamiento', models.BooleanField(default=False, verbose_name='equipamiento')),
                ('renovacion', models.BooleanField(default=False, verbose_name='equipamiento')),
                ('creada_por', models.ForeignKey(default=49, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tipo de salida',
                'verbose_name_plural': 'Tipos de salida',
            },
        ),
        migrations.CreateModel(
            name='SolicitudMovimientoBeqt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(default=django.utils.timezone.now)),
                ('cantidad', models.PositiveIntegerField()),
                ('terminada', models.BooleanField(default=False)),
                ('recibida', models.BooleanField(default=False)),
                ('devolucion', models.BooleanField(default=False)),
                ('rechazar', models.BooleanField(default=False)),
                ('desecho', models.BooleanField(default=False)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('autorizada_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='autorizaciones_movimiento_beqt', to=settings.AUTH_USER_MODEL)),
                ('creada_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='solicitudes_movimiento_beqt', to=settings.AUTH_USER_MODEL)),
                ('etapa_final', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='solicitudes_final_beqt', to='inventario.DispositivoEtapa')),
                ('etapa_inicial', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='solicitudes_inicial_beqt', to='inventario.DispositivoEtapa')),
                ('no_salida', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='salida_inventario_beqt', to='beqt.SalidaInventario')),
                ('recibida_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='recibida_por_beqt', to=settings.AUTH_USER_MODEL)),
                ('tipo_dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.DispositivoTipo')),
            ],
            options={
                'verbose_name': 'Solicitud de movimiento',
                'verbose_name_plural': 'Solicitudes de movimiento',
            },
        ),
        migrations.CreateModel(
            name='AccessPointBeqt',
            fields=[
                ('dispositivobeqt_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='beqt.DispositivoBeqt')),
                ('indice', models.PositiveIntegerField(editable=False, unique=True)),
                ('cantidad_puertos', models.PositiveIntegerField(blank=True, null=True)),
                ('velocidad', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Access Point',
                'verbose_name_plural': 'Access Point',
            },
            bases=('beqt.dispositivobeqt',),
        ),
        migrations.CreateModel(
            name='HDDBeqt',
            fields=[
                ('dispositivobeqt_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='beqt.DispositivoBeqt')),
                ('indice', models.PositiveIntegerField(editable=False, unique=True)),
                ('capacidad', models.PositiveIntegerField(blank=True, null=True)),
                ('asignado', models.BooleanField(default=False)),
                ('medida', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.DispositivoMedida')),
                ('puerto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hdds_beqt', to='inventario.DispositivoPuerto')),
            ],
            options={
                'verbose_name': 'HDD',
                'ordering': ['indice'],
                'db_table': 'dispositivo_hdd_beqt',
                'verbose_name_plural': 'HDDs',
            },
            bases=('beqt.dispositivobeqt',),
        ),
        migrations.CreateModel(
            name='LaptopBeqt',
            fields=[
                ('dispositivobeqt_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='beqt.DispositivoBeqt')),
                ('indice', models.PositiveIntegerField(editable=False, unique=True)),
                ('ram', models.PositiveIntegerField(blank=True, null=True)),
                ('pulgadas', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('servidor', models.BooleanField(default=False)),
                ('disco_duro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laptops_beqt', to='beqt.HDDBeqt')),
                ('procesador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventario.Procesador')),
                ('ram_medida', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.DispositivoMedida')),
                ('version_sistema', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventario.VersionSistema')),
            ],
            options={
                'verbose_name': 'Laptop',
                'ordering': ['indice'],
                'db_table': 'dispositivo_laptop_beqt',
                'verbose_name_plural': 'Laptops',
            },
            bases=('beqt.dispositivobeqt',),
        ),
        migrations.CreateModel(
            name='TabletBeqt',
            fields=[
                ('dispositivobeqt_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='beqt.DispositivoBeqt')),
                ('indice', models.PositiveIntegerField(editable=False, unique=True)),
                ('almacenamiento', models.PositiveIntegerField(blank=True, null=True)),
                ('pulgadas', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('ram', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('almacenamiento_externo', models.BooleanField(default=False)),
                ('medida_almacenamiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='almacenamiento_tablets_beqt', to='inventario.DispositivoMedida')),
                ('medida_ram', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ram_tables_beqt', to='inventario.DispositivoMedida')),
                ('procesador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.Procesador')),
                ('so_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='so_tablets_beqt', to='inventario.Software')),
                ('version_sistema', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='versiones_tablets_beqt', to='inventario.VersionSistema')),
            ],
            options={
                'verbose_name': 'Tablet',
                'ordering': ['indice'],
                'db_table': 'dispositivo_tablet_beqt',
                'verbose_name_plural': 'Tablets',
            },
            bases=('beqt.dispositivobeqt',),
        ),
        migrations.AddField(
            model_name='salidainventario',
            name='tipo_salida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='beqt.SalidaTipoBeqt'),
        ),
        migrations.AddField(
            model_name='salidacomentariobeqt',
            name='salida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_beqt', to='beqt.SalidaInventario'),
        ),
        migrations.AddField(
            model_name='revisionsalidabeqt',
            name='salida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='revisiones_beqt', to='beqt.SalidaInventario'),
        ),
        migrations.AddField(
            model_name='revisionsalidabeqt',
            name='tecnico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tecnicos_beqt', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='revisioncomentariobeqt',
            name='revision',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_beqt', to='beqt.RevisionSalidaBeqt'),
        ),
        migrations.AddField(
            model_name='paquetebeqt',
            name='salida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='paquetes_beqt', to='beqt.SalidaInventario'),
        ),
        migrations.AddField(
            model_name='paquetebeqt',
            name='tipo_paquete',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='paquetes_beqt', to='beqt.PaqueteTipoBeqt'),
        ),
        migrations.AddField(
            model_name='dispositivopaquete',
            name='dispositivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='asignacion_beqt', to='beqt.DispositivoBeqt'),
        ),
        migrations.AddField(
            model_name='dispositivopaquete',
            name='paquete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='asignacion_beqt', to='beqt.PaqueteBeqt'),
        ),
        migrations.AddField(
            model_name='dispositivofalla',
            name='dispositivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fallas_beqt', to='beqt.DispositivoBeqt'),
        ),
        migrations.AddField(
            model_name='dispositivofalla',
            name='reparada_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fallas_reparadas_beqt', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dispositivofalla',
            name='reportada_por',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fallas_reportadas_beqt', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dispositivobeqt',
            name='clase',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clase_dispositivos_beqt', to='inventario.DispositivoClase'),
        ),
        migrations.AddField(
            model_name='dispositivobeqt',
            name='creada_por',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dispositivobeqt',
            name='entrada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dispositivos_beqt', to='beqt.Entrada'),
        ),
        migrations.AddField(
            model_name='dispositivobeqt',
            name='entrada_detalle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='detalle_dispositivos', to='beqt.EntradaDetalleBeqt'),
        ),
        migrations.AddField(
            model_name='dispositivobeqt',
            name='estado',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.DispositivoEstado'),
        ),
        migrations.AddField(
            model_name='dispositivobeqt',
            name='etapa',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventario.DispositivoEtapa'),
        ),
        migrations.AddField(
            model_name='dispositivobeqt',
            name='marca',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.DispositivoMarca'),
        ),
        migrations.AddField(
            model_name='dispositivobeqt',
            name='tarima',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dispositivos_beqt', to='inventario.Tarima'),
        ),
        migrations.AddField(
            model_name='dispositivobeqt',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.DispositivoTipo'),
        ),
        migrations.AddField(
            model_name='cambioetapabeqt',
            name='dispositivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cambios_etapa_beqt', to='beqt.DispositivoBeqt'),
        ),
        migrations.AddField(
            model_name='cambioetapabeqt',
            name='etapa_final',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cambios_final_beqt', to='inventario.DispositivoEtapa'),
        ),
        migrations.AddField(
            model_name='cambioetapabeqt',
            name='etapa_inicial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cambios_inicio_beqt', to='inventario.DispositivoEtapa'),
        ),
        migrations.AddField(
            model_name='cambioetapabeqt',
            name='solicitud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cambios_beqt', to='beqt.SolicitudMovimientoBeqt'),
        ),
        migrations.AddField(
            model_name='cambioestadobeqt',
            name='dispositivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cambios_estado_beqt', to='beqt.DispositivoBeqt'),
        ),
        migrations.AddField(
            model_name='cambioestadobeqt',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cambios_beqt', to='inventario.DispositivoEstado'),
        ),
        migrations.AlterUniqueTogether(
            name='paquetebeqt',
            unique_together=set([('salida', 'indice')]),
        ),
        migrations.AddIndex(
            model_name='dispositivobeqt',
            index=models.Index(fields=['triage'], name='beqt_dispos_triage_1293ed_idx'),
        ),
        migrations.AddField(
            model_name='accesspointbeqt',
            name='puerto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.DispositivoPuerto'),
        ),
        migrations.AddField(
            model_name='accesspointbeqt',
            name='velocidad_medida',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.DispositivoMedida'),
        ),
        migrations.AddIndex(
            model_name='tabletbeqt',
            index=models.Index(fields=['indice'], name='dispositivo_indice_90dd02_idx'),
        ),
        migrations.AddIndex(
            model_name='laptopbeqt',
            index=models.Index(fields=['indice'], name='dispositivo_indice_0460ea_idx'),
        ),
        migrations.AddIndex(
            model_name='hddbeqt',
            index=models.Index(fields=['indice'], name='dispositivo_indice_a20767_idx'),
        ),
    ]
