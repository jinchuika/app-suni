#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import uuid
import qrcode
import json
import sys
from io import BytesIO
from django.db import models
from django.db.utils import OperationalError
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from easy_thumbnails import fields as et_fields

from apps.inventario import transacciones
from apps.crm import models as crm_m
from apps.tpe import models as tpe_m
from apps.escuela import models as escuela_m


class EntradaTipo(models.Model):

    """Para indicar el tipo de :class:`Entrada`.
    El campo `contable` indica que los detalles de entrada deben asignar precio.
    """

    nombre = models.CharField(max_length=25)
    contable = models.BooleanField(default=False)
    contenedor = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tipo de entrada"
        verbose_name_plural = "Tipos de entrada"

    def __str__(self):
        return self.nombre


class EntradaEstado(models.Model):

    """Para indicar si está en creación, completada o cancelada.
    """

    nombre = models.CharField(max_length=45)

    class Meta:
        verbose_name = "Estado de entrada"
        verbose_name_plural = "Estados de entrada"

    def __str__(self):
        return self.nombre


class Entrada(models.Model):

    """Cualquier vía por la cual puede ingresar equipo al inventario.
    """

    tipo = models.ForeignKey(EntradaTipo, on_delete=models.PROTECT, related_name='entradas')
    fecha = models.DateField()
    fecha_cierre = models.DateField(blank=True, null=True)
    en_creacion = models.BooleanField(default=True)
    creada_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entradas_creadas')
    recibida_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entradas_recibidas')
    proveedor = models.ForeignKey(crm_m.Donante, on_delete=models.PROTECT, related_name='entradas')
    factura = models.PositiveIntegerField(default=0)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"

    def __str__(self):
        return str(self.id)

    @property
    def descontado(self):
        return self.subtotal - sum(d.monto for d in self.descuentos.all())

    @property
    def subtotal(self):
        return sum(d.precio_subtotal for d in self.detalles.all() if d.precio_subtotal)

    @property
    def total(self):
        return sum(d.precio_total for d in self.detalles.all())

    def get_absolute_url(self):
        return reverse_lazy('entrada_update', kwargs={'pk': self.id})


class DispositivoTipo(models.Model):

    """Tipo de un :class:`Dispositivo`s
    En caso de que se marque `usa_triage` como `True`, el `slug` debe coincidir con
    los SLUG disponibles en los modelos que heredan :class:`Dispositivo`.
    """

    tipo = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    usa_triage = models.BooleanField(default=False)
    conta = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tipo de dispositivo"
        verbose_name_plural = "Tipos de dispositivo"
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.tipo

    def save(self, *args, **kwargs):
        """Valida que los los :class:`DispositivoTipo` que `usa_triage` tengan un `slug` valido.
        """
        if self.usa_triage:
            lista_slug = [m.SLUG_TIPO for m in Dispositivo.__subclasses__()]
            if self.slug not in lista_slug:
                raise ValidationError(
                    ('El slug ingresado no coincide con los disponibles. Las opciones son: {}'.format(lista_slug)),
                    code='entrada_precio_total')
        super(DispositivoTipo, self).save(*args, **kwargs)


class EntradaDetalle(models.Model):

    """Detalle que indica la cantidad de cada tipo de equipo que ingresa en la :class:`Entrada`.
    Los campos de contabilidad indican el precio al ingresa el equipo cuando la entrada es una compra.
    El usuario ingresa el subtotal, el `precio_unitario` será calculado al dividir `precio_subtotal` / `total`.
    Los descuentos que se apliquen a la Entrada afectarán en el `precio_unitario`, por lo que ese dato
    se almacena en `precio_descontado`.

    El `precio_total` se calcula a partir de `precio_descontado` * `total`.
    """

    # Campos sobre inventario
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name='detalles')
    tipo_dispositivo = models.ForeignKey(DispositivoTipo, on_delete=models.PROTECT, related_name='detalles_entrada')
    util = models.PositiveIntegerField(default=0)
    repuesto = models.PositiveIntegerField(default=0)
    desecho = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=50)
    dispositivos_creados = models.BooleanField(default=False, blank=True, verbose_name='Dispositivos creados')
    repuestos_creados = models.BooleanField(default=False, blank=True, verbose_name='Repuestos creados')
    qr_repuestos = models.BooleanField(default=False, blank=True, verbose_name='Imprimir Qr Repuesto')
    qr_dispositivo = models.BooleanField(default=False, blank=True, verbose_name='Imprimir Qr Dispositivo')
    impreso = models.BooleanField(default=False, blank=True, verbose_name='Impreso')
    # Creacion de fechas
    fecha_dispositivo = models.DateField(blank=True, null=True)
    fecha_repuesto = models.DateField(blank=True, null=True)
    # Campos sobre contabilidad
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    precio_subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    precio_descontado = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Registro
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    # Kardex
    enviar_kardex = models.BooleanField(default=False, blank=True, verbose_name='kardex')
    ingresado_kardex = models.BooleanField(default=False, blank=True, verbose_name='Guardar en kardex')
    proveedor_kardex = models.ForeignKey(
        'kardex.Proveedor',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='proveedor_kardex')
    estado_kardex = models.ForeignKey(
        'kardex.EstadoEquipo',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='estado_kardex')
    tipo_entrada_kardex = models.ForeignKey(
        'kardex.TipoEntrada',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='tipo_entrada_kardex')

    class Meta:
        verbose_name = "Detalle de entrada"
        verbose_name_plural = "Detalles de entrada"

    def __str__(self):
        return '{entrada} - {tipo}'.format(
            entrada=self.entrada,
            tipo=self.tipo_dispositivo)

    def inventario_desecho(self):
        queryset = self.detalle_entrada.all()
        return sum(detalle.cantidad for detalle in queryset)

    @property
    def existencia_desecho(self):
        return self.desecho - self.inventario_desecho()

    def save(self, *args, **kwargs):
        """Se debe validar que el detalle de una entrada que involucre precio, por ejemplo, una compra,
        incluya el precio total.

        Los valores de los campos `precio_unitario` y `precio_descontado` pueden cambiar dependiendo de
        los descuentos que hayan sido aplicados a la entrada.
        El cálculo de todos los campos se realiza desde las funciones definidas en `signals.py`.
        """
        if self.tipo_dispositivo.usa_triage is False:
            self.dispositivos_creados = True
            self.repuestos_creados = True
            self.enviar_kardex = True
        if self.entrada.tipo.contable and not self.precio_subtotal:
            raise ValidationError(
                'El tipo de entrada requiere un precio total', code='entrada_precio_total')

        super(EntradaDetalle, self).save(*args, **kwargs)

    def crear_dispositivos(self, util=None):
        if util is None:
            util = self.util
        # Busca el modelo del `tipo_dispositivo` del objeto actual
        modelo = Dispositivo.obtener_modelo_hijo(self.tipo_dispositivo)
        creados = 0
        errores = 0
        for _ in range(0, util):
            try:
                transacciones.ingresar_dispositivo(
                    entrada=self.entrada,
                    modelo=modelo,
                    tipo=self.tipo_dispositivo,
                    entrada_detalle=self,
                    precio=self.precio_unitario
                    )
                creados = creados + 1
            except OperationalError:
                errores = errores + 1
        return {'creados': creados, 'errores': errores}

    def crear_repuestos(self, repuesto=None):
        if repuesto is None:
            repuesto = self.repuesto
        creados = 0
        errores = 0
        estado_repuesto = RepuestoEstado.objects.first()
        for _ in range(0, repuesto):
            try:
                transacciones.ingresar_repuesto(
                    entrada=self.entrada,
                    modelo_repuesto=Repuesto,
                    estado=estado_repuesto,
                    tipo=self.tipo_dispositivo,
                    entrada_detalle=self,
                    precio=self.precio_unitario
                )
                creados = creados + 1
            except OperationalError:
                errores = errores + 1
        return {'creados': creados, 'errores': errores}

    def get_absolute_url(self):
        return self.entrada.get_absolute_url()

class DescuentoEntrada(models.Model):
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name='descuentos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "DescuentoEntrada"
        verbose_name_plural = "DescuentoEntradas"

    def __str__(self):
        return str(self.entrada)

    def get_absolute_url(self):
        return self.entrada.get_absolute_url()


class DispositivoEstado(models.Model):

    """Estado de un :class:`Dispositivo`. Indica que el dispositivo puede estar en cualquiera de los siguientes estados:
        - Pendiente: aun no ha sido reparado ni desechado
        - Bueno: ya fue reparado
        - Desechado: ha sido desechado por un técnico
        - Entregado: enviado a una escuela
    """
    PD = 1
    BN = 2
    DS = 3
    EN = 4

    estado = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Estado de dispositivo"
        verbose_name_plural = "Estados de dispositivo"

    def __str__(self):
        return self.estado


class DispositivoEtapa(models.Model):

    """Etapa de un :class:`Dispositivo`. Indica la parte del proceso de manufactura por la que puede pasar el dispositivo.
    A continuación se detalla la etapa y los estados que admite:
        - Almacenado en bodega: almacenamiento sin importar el estado (pendiente, bueno)
        - Tránsito: en reparación (pendiente, bueno)
        - Control de calidad: listo para asignación para ser enviado a una escuela (bueno)
        - Desechado: enviado a desecho (desechado)
        - Listo: aprobado por control de calidad (bueno)
        - Entregado: uubicado en una escuela después de una salida aprobada (entregado)

    El campo de estados disponibles indica qué :class:`DispositivoEstado` admite este proceso.
    """
    AB = 1  # Almacenado
    TR = 2  # Tránsito
    CC = 3  # Control de calidad
    DS = 4  # Desecho
    LS = 5  # Listo
    EN = 6  # Entregado

    proceso = models.CharField(max_length=30)
    estados_disponibles = models.ManyToManyField(DispositivoEstado)

    class Meta:
        verbose_name = "Etapa de dispositivo"
        verbose_name_plural = "Etapas de dispositivo"

    def __str__(self):
        return self.proceso


class DispositivoMarca(models.Model):

    """Marca de un :class:`Dispositivo`
    """

    marca = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Marca de dispositivo"
        verbose_name_plural = "Marcas de dispositivo"

    def __str__(self):
        return self.marca


class DispositivoModelo(models.Model):

    """Modelo de un :class:`Dispositivo`
    """

    modelo = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Modelo de dispositivo"
        verbose_name_plural = "Modelos de dispositivo"

    def __str__(self):
        return self.modelo


class Pasillo(models.Model):
    pass

    def __str__(self):
        return str(self.id)

    def tarimas(self):
        return Tarima.objects.filter(sector__nivel__pasillo=self)

    def dispositivo(self):
        return Dispositivo.objects.filter(tarima__sector__nivel__pasillo=self)


class Nivel(models.Model):
    nivel = models.CharField(max_length=1)
    pasillo = models.ForeignKey(Pasillo, on_delete=models.PROTECT, related_name='niveles')

    def __str__(self):
        return '{}{}'.format(self.pasillo, self.nivel)

    def tarimas(self):
        return Tarima.objects.filter(sector__nivel=self)


class Sector(models.Model):
    sector = models.IntegerField(null=False)
    nivel = models.ForeignKey(Nivel, related_name='sectores')
    codigo_qr = et_fields.ThumbnailerImageField(upload_to='qr_sector', blank=True, null=True, editable=False)

    def __str__(self):
        return '{nivel}-{sector}'.format(nivel=self.nivel, sector=self.sector)

    def get_absolute_url(self):
        return reverse_lazy('sector_update', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        super(Sector, self).save(*args, **kwargs)
        if not self.codigo_qr:
            self.crear_qrcode()
            super(Sector, self).save(*args, **kwargs)

    def crear_qrcode(self):
        """Genera le código QR para apuntar a la id del sector
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=1,
        )
        data_qr = {
            'tipo': 'sector',
            'id': self.id
        }
        qr.add_data(json.dumps(data_qr, ensure_ascii=False))
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer)
        filename = 'sector-{}.png'.format(self.id)
        filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.getbuffer().nbytes, None)
        self.codigo_qr.save(filename, filebuffer)


class Tarima(models.Model):
    sector = models.ForeignKey(
        Sector,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='tarimas'
    )
    codigo_qr = et_fields.ThumbnailerImageField(upload_to='qr_tarima', blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super(Tarima, self).save(*args, **kwargs)
        if not self.codigo_qr:
            self.crear_qrcode()
            super(Tarima, self).save(*args, **kwargs)

    def crear_qrcode(self):
        """Genera le código QR para apuntar a la id de la tarima
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=1,
        )
        data_qr = {
            'tipo': 'tarima',
            'id': self.id
        }
        qr.add_data(json.dumps(data_qr, ensure_ascii=False))
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer)
        filename = 'tarima-{}.png'.format(self.id)
        filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.getbuffer().nbytes, None)
        self.codigo_qr.save(filename, filebuffer)


class Dispositivo(models.Model):

    """Cualquier elemento almacenado en la base de datos de inventario que puede ser entregado a una escuela.
    No debe existir una instancia de este modelo sin un objeto heredado del mismo.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    triage = models.SlugField(unique=True, blank=True, editable=False)
    tipo = models.ForeignKey(DispositivoTipo, on_delete=models.CASCADE)
    entrada = models.ForeignKey(Entrada, on_delete=models.PROTECT, related_name='dispositivos')
    entrada_detalle = models.ForeignKey(
        EntradaDetalle,
        on_delete=models.PROTECT,
        null=True,
        related_name='detalle_dispositivos')
    impreso = models.BooleanField(default=False, blank=True, verbose_name='Impreso')
    estado = models.ForeignKey(
        DispositivoEstado,
        on_delete=models.CASCADE,
        null=True,
        editable=True,
        default=DispositivoEstado.PD
    )
    etapa = models.ForeignKey(
        DispositivoEtapa,
        on_delete=models.PROTECT,
        null=True,
        editable=True,
        default=DispositivoEtapa.AB
    )

    marca = models.ForeignKey(DispositivoMarca, on_delete=models.CASCADE, null=True, blank=True)
    modelo = models.CharField(max_length=80, null=True, blank=True)
    serie = models.CharField(max_length=80, null=True, blank=True)
    codigo_qr = et_fields.ThumbnailerImageField(upload_to='qr_dispositivo', blank=True, null=True)
    tarima = models.ForeignKey(Tarima, on_delete=models.PROTECT, blank=True, null=True, related_name='dispositivos')
    valido = models.BooleanField(default=True, blank=True, verbose_name='Válido')
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
        indexes = [
            models.Index(fields=['triage']),
        ]

    def __str__(self):
        return str(self.triage)

    def save(self, *args, **kwargs):
        super(Dispositivo, self).save(*args, **kwargs)
        if not self.codigo_qr:
            self.crear_qrcode()
            super(Dispositivo, self).save(*args, **kwargs)

    def get_absolute_url(self):
        cast = self.cast()
        if cast:
            return cast.get_absolute_url()
        else:
            return ''

    def cast(self):
        """Se encarga de obtener el dispositivo del modelo que ha heredado este objeto.
        Por ejemplo, el CPU-1, M-3, etc.
        """
        for name in dir(self):
            try:
                attr = getattr(self, name)
                if isinstance(attr, self.__class__) and type(attr) != type(self):
                    return attr
            except:
                print("Error al cargar el modelo de {}".format(self.tipo))

    def crear_qrcode(self):
        """Genera le código QR para apuntar a la id del dispositivo
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=1,
        )
        data_qr = {
            'id': str(self.id),
            'triage': self.triage,
            'tipo': str(self.tipo)
        }
        qr.add_data(json.dumps(data_qr, ensure_ascii=False))
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer)
        filename = 'dispositivo-{}.png'.format(self.id)
        filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.getbuffer().nbytes, None)
        self.codigo_qr.save(filename, filebuffer)

    @classmethod
    def obtener_modelo_hijo(cls, tipo_dispositivo):
        """Obtiene el modelo hijo de `Dispositivo` a partir de un `DispositivoTipo`"""
        modelo = next(
            (
                f.related_model for f in cls._meta.get_fields()
                if f.one_to_one and f.related_model.SLUG_TIPO == tipo_dispositivo.slug
            ),
            None
        )
        if modelo is None:
            raise OperationalError('No es un dispositivo')
        return modelo


class DispositivoFalla(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='fallas')
    descripcion_falla = models.TextField(verbose_name='Descripción de la falla')
    descripcion_solucion = models.TextField(null=True, blank=True, verbose_name='Descripción de la solución')
    fecha_inicio = models.DateTimeField(default=timezone.now, verbose_name='Fecha de inicio')
    fecha_fin = models.DateTimeField(blank=True, verbose_name='Fecha de fin', null=True)
    terminada = models.BooleanField(default=False, blank=True)
    reportada_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='fallas_reportadas')
    reparada_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='fallas_reparadas',
        null=True,
        blank=True)

    class Meta:
        verbose_name = "DispositivoFalla"
        verbose_name_plural = "DispositivoFallas"

    def __str__(self):
        return 'F-{pk}'.format(pk=self.id)

    def get_absolute_url(self):
        return self.dispositivo.get_absolute_url()


class SoftwareTipo(models.Model):

    """Para indicar si es aplicación, sistema operativo, etc.
    """

    tipo = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Tipo de software"
        verbose_name_plural = "Tipos de software"

    def __str__(self):
        return self.tipo


class Software(models.Model):

    """Cualquier software que se pueda instalar en un :class:`Dispositivo` de cualquier tipo.
    """

    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(SoftwareTipo, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Software"
        verbose_name_plural = "Software"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('software_detail', kwargs={'pk': self.id})


class VersionSistema(models.Model):

    """Imagen de un sistema instalable en un :class:`Dispositivo`.
    Incluye el sistema operativo y los programas o aplicaciones que se instalen.
    """

    nombre = models.CharField(max_length=55)
    so = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='versiones')
    software = models.ManyToManyField(Software, blank=True)

    class Meta:
        verbose_name = "Versión de sistema"
        verbose_name_plural = "Versiones de sistema"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('versionsistema_detail', kwargs={'pk': self.id})


class PuertoTipo(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Tipo de puerto"
        verbose_name_plural = "Tipos de puerto"

    def __str__(self):
        return self.nombre


class DispositivoPuerto(models.Model):

    """Puerto de cualquier tipo de :class:`Dispositivo`.
    """

    nombre = models.CharField(max_length=15)
    tipo = models.ForeignKey(PuertoTipo, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Puerto"
        verbose_name_plural = "Puertos"

    def __str__(self):
        return self.nombre


class DispositivoMedida(models.Model):

    """Medida de cualquier tipo de :class:`Dispositivo` (GB, GH, Mbps, etc)
    """

    nombre = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Medida"
        verbose_name_plural = "Medidas"

    def __str__(self):
        return self.nombre


class Teclado(Dispositivo):
    SLUG_TIPO = 'T'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    puerto = models.ForeignKey(
        DispositivoPuerto,
        on_delete=models.CASCADE,
        related_name='teclados',
        null=True,
        blank=True)
    caja = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = "Teclado"
        verbose_name_plural = "Teclados"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_teclado'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('teclado_detail', kwargs={'triage': self.triage})


class MouseTipo(models.Model):

    """Para indicar si es mecánico, óptico o cualquier tipo futuro.
    """

    tipo = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Tipo de mouse"
        verbose_name_plural = "Tipos de mouse"

    def __str__(self):
        return self.tipo


class Mouse(Dispositivo):
    SLUG_TIPO = 'S'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    puerto = models.ForeignKey(
        DispositivoPuerto,
        on_delete=models.CASCADE,
        related_name='mouses',
        null=True,
        blank=True)
    tipo_mouse = models.ForeignKey(MouseTipo, on_delete=models.CASCADE, null=True, blank=True)
    caja = models.CharField(max_length=30,  null=True, blank=True)

    class Meta:
        verbose_name = "Mouse"
        verbose_name_plural = "Mouses"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_mouse'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('mouse_detail', kwargs={'triage': self.triage})


class HDD(Dispositivo):
    SLUG_TIPO = 'HDD'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    puerto = models.ForeignKey(
        DispositivoPuerto,
        on_delete=models.CASCADE,
        related_name='hdds',
        null=True,
        blank=True)
    capacidad = models.PositiveIntegerField(null=True, blank=True)
    medida = models.ForeignKey(DispositivoMedida, null=True, blank=True)

    class Meta:
        verbose_name = "HDD"
        verbose_name_plural = "HDDs"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_hdd'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('hdd_detail', kwargs={'triage': self.triage})

    @property
    def en_uso(self):
        """Indica si fue asignado a un :class:`CPU` o :class:`Laptop`

        Returns:
            bool
        """
        return self.cpus.count() > 0 or self.laptops.count() > 0


class Procesador(models.Model):
    nombre = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Procesador"
        verbose_name_plural = "Procesadores"

    def __str__(self):
        return self.nombre


class Tablet(Dispositivo):
    SLUG_TIPO = 'B'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    version_sistema = models.ForeignKey(VersionSistema, related_name='versiones_tablets', null=True, blank=True)
    so_id = models.ForeignKey(Software, related_name='so_tablets', null=True, blank=True)
    almacenamiento = models.PositiveIntegerField(null=True, blank=True)
    medida_almacenamiento = models.ForeignKey(
        DispositivoMedida,
        blank=True,
        null=True,
        related_name='almacenamiento_tablets')
    pulgadas = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    procesador = models.ForeignKey(Procesador, blank=True, null=True)
    ram = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    medida_ram = models.ForeignKey(DispositivoMedida, null=True, blank=True, related_name='ram_tables')
    almacenamiento_externo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tablet"
        verbose_name_plural = "Tablets"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_tablet'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('tablet_detail', kwargs={'triage': self.triage})


class MonitorTipo(models.Model):

    """Para indicar si un :class:`Monitor` puede ser CRT, LCD, LED.
    """

    tipo = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Tipo de monitor"
        verbose_name_plural = "Tipos de monitor"

    def __str__(self):
        return self.tipo


class Monitor(Dispositivo):
    SLUG_TIPO = 'M'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    tipo_monitor = models.ForeignKey(MonitorTipo, on_delete=models.PROTECT, null=True, blank=True)
    puerto = models.ForeignKey(
        DispositivoPuerto,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='monitores')
    pulgadas = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    class Meta:
        verbose_name = "Monitor"
        verbose_name_plural = "Monitores"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_monitor'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('monitor_detail', kwargs={'triage': self.triage})


class CPU(Dispositivo):
    SLUG_TIPO = 'CPU'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    procesador = models.ForeignKey(Procesador, on_delete=models.PROTECT, null=True, blank=True)
    version_sistema = models.ForeignKey(VersionSistema, on_delete=models.PROTECT, null=True, blank=True)
    disco_duro = models.ForeignKey(HDD, on_delete=models.PROTECT, null=True, blank=True, related_name='cpus')
    ram = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ram_medida = models.ForeignKey(DispositivoMedida, null=True, blank=True)
    servidor = models.BooleanField(default=False)
    all_in_one = models.BooleanField(default=False)

    class Meta:
        verbose_name = "CPU"
        verbose_name_plural = "CPUs"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_cpu'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('cpu_detail', kwargs={'triage': self.triage})


class Laptop(Dispositivo):
    SLUG_TIPO = 'L'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    procesador = models.ForeignKey(Procesador, on_delete=models.PROTECT, null=True, blank=True)
    version_sistema = models.ForeignKey(VersionSistema, on_delete=models.PROTECT, null=True, blank=True)
    disco_duro = models.ForeignKey(HDD, on_delete=models.PROTECT, null=True, blank=True, related_name='laptops')
    ram = models.PositiveIntegerField(null=True, blank=True)
    ram_medida = models.ForeignKey(DispositivoMedida, null=True, blank=True)
    pulgadas = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    class Meta:
        verbose_name = "Laptop"
        verbose_name_plural = "Laptops"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_laptop'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('laptop_detail', kwargs={'triage': self.triage})


class TipoRed(models.Model):
    nombre = models.CharField(max_length=45)

    class Meta:
        verbose_name = "Tipo de dispositivo de red"
        verbose_name_plural = "Tipos de dispositivos de red"

    def __str__(self):
        return self.nombre


class DispositivoRed(Dispositivo):
    SLUG_TIPO = 'R'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    cantidad_puertos = models.PositiveIntegerField(null=True, blank=True)
    puerto = models.ForeignKey(DispositivoPuerto, null=True, blank=True)
    velocidad = models.PositiveIntegerField(null=True, blank=True)
    velocidad_medida = models.ForeignKey(DispositivoMedida, null=True, blank=True)

    class Meta:
        verbose_name = "Dispositivo de red"
        verbose_name_plural = "Dispositivos de red"

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('red_detail', kwargs={'triage': self.triage})


class AccessPoint(Dispositivo):
    SLUG_TIPO = 'AP'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    cantidad_puertos = models.PositiveIntegerField(null=True, blank=True)
    puerto = models.ForeignKey(DispositivoPuerto, null=True, blank=True)
    velocidad = models.PositiveIntegerField(null=True, blank=True)
    velocidad_medida = models.ForeignKey(DispositivoMedida, null=True, blank=True)

    class Meta:
        verbose_name = "Access Point"
        verbose_name_plural = "Access Point"

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('ap_detail', kwargs={'triage': self.triage})


class RepuestoEstado(models.Model):

    """Indica si el repuesto puede ser:
    - Almacenaje
    - Utilizado
    - Desechado
    """

    nombre = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Estado de repuesto"
        verbose_name_plural = "Estados de repuesto"

    def __str__(self):
        return self.nombre


class Repuesto(models.Model):
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name='repuestos')
    entrada_detalle = models.ForeignKey(
        EntradaDetalle,
        on_delete=models.PROTECT,
        null=True,
        related_name='detalle_repuesto')
    impreso = models.BooleanField(default=False, blank=True, verbose_name='Impreso')
    tipo = models.ForeignKey(DispositivoTipo, on_delete=models.PROTECT, related_name='repuestos')
    estado = models.ForeignKey(RepuestoEstado, on_delete=models.PROTECT)
    descripcion = models.TextField(null=True, blank=True)
    disponible = models.BooleanField(default=False)
    codigo_qr = et_fields.ThumbnailerImageField(upload_to='qr_repuestos', blank=True, null=True)
    tarima = models.ForeignKey(Tarima, on_delete=models.PROTECT, blank=True, null=True, related_name='repuestos')
    valido = models.BooleanField(default=True, blank=True, verbose_name='Válido')
    marca = models.ForeignKey(DispositivoMarca, on_delete=models.CASCADE, null=True, blank=True)
    modelo = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        verbose_name = "Repuesto"
        verbose_name_plural = "Repuestos"

    def __str__(self):
        return 'R-{}'.format(self.id)

    def save(self, *args, **kwargs):
        super(Repuesto, self).save(*args, **kwargs)
        if not self.codigo_qr:
            self.crear_qrcode()
            super(Repuesto, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('repuesto_detail', kwargs={'pk': self.id})

    def crear_qrcode(self):
        """Genera le código QR para apuntar a la id del repuesto
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=1,
        )
        data_qr = {
            'id': str(self.id),
            'tipo': str(self.tipo)
        }
        qr.add_data(json.dumps(data_qr, ensure_ascii=False))
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer)
        filename = 'repuesto-{}.png'.format(self.id)
        filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.getbuffer().nbytes, None)
        self.codigo_qr.save(filename, filebuffer)


class DispositivoRepuesto(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(default=timezone.now)
    asignado_por = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Repuesto de dispositivo"
        verbose_name_plural = "Repuestos de dispositivo"

    def __str__(self):
        return '{} -> {}'.format(self.repuesto, self.dispositivo)


class DesechoEmpresa(models.Model):
    nombre = models.CharField(max_length=50)
    encargado = models.CharField(max_length=100)
    telefono = models.IntegerField(verbose_name="Número Telefónico")
    dpi = models.CharField(max_length=14)

    class Meta:
        verbose_name = "Empresa de desecho"
        verbose_name_plural = "Empresas de desecho"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('desechoempresa_update', kwargs={'pk': self.id})


class DesechoSalida(models.Model):
    fecha = models.DateField(default=timezone.now)
    empresa = models.ForeignKey(DesechoEmpresa, on_delete=models.PROTECT, related_name='salidas')
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    peso = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Peso (libras)', default=0.0)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    observaciones = models.TextField(null=True, blank=True)
    en_creacion = models.BooleanField(default=True, blank=True, verbose_name='En creación')
    url = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Salida de desecho"
        verbose_name_plural = "Salidas de desecho"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('desechosalida_update', kwargs={'pk': self.id})


class DesechoDetalle(models.Model):
    desecho = models.ForeignKey(DesechoSalida, on_delete=models.PROTECT, related_name='detalles')
    entrada_detalle = models.ForeignKey(
        EntradaDetalle,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="detalle_entrada")
    cantidad = models.PositiveIntegerField(default=0)
    tipo_dispositivo = models.ForeignKey(DispositivoTipo, on_delete=models.PROTECT, related_name='salidas_desecho')
    aprobado = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = "Detalle de salida de desecho"
        verbose_name_plural = "Detalles de salida de desecho"

    def __str__(self):
        return '{desecho} {entrada}'.format(
            desecho=self.desecho,
            entrada=self.entrada_detalle)

class DesechoDispositivo(models.Model):
    desecho = models.ForeignKey(DesechoSalida, on_delete=models.PROTECT, related_name='detalles_dispositivos')
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='desecho')
    aprobado = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = "Dispositivo de desecho"
        verbose_name_plural = "Dispositivos de desecho"

    def __str__(self):
        return '{desecho} -> {dispositivo}'.format(
            desecho=self.desecho,
            dispositivo=self.dispositivo)


class SalidaTipo(models.Model):
    nombre = models.CharField(max_length=30)
    necesita_revision = models.BooleanField(default=True, blank=True, verbose_name='Necesita revisión')
    especial = models.BooleanField(default=False, blank=True, verbose_name='especial')

    class Meta:
        verbose_name = "Tipo de salida"
        verbose_name_plural = "Tipos de salida"

    def __str__(self):
        return self.nombre


class SalidaEstado(models.Model):

    """Para indicar si está en Pendiende, Listo o Entregado
    """

    nombre = models.CharField(max_length=45)

    class Meta:
        verbose_name = "Estado de salida"
        verbose_name_plural = "Estados de salida"

    def __str__(self):
        return self.nombre


class SalidaInventario(models.Model):
    tipo_salida = models.ForeignKey(SalidaTipo, on_delete=models.PROTECT)
    fecha = models.DateField(default=timezone.now)
    creada_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='salidas')
    en_creacion = models.BooleanField(default=True, verbose_name='En creación')
    entrega = models.BooleanField(default=True, verbose_name="Es entrega", blank=True)
    escuela = models.ForeignKey(
        escuela_m.Escuela,
        on_delete=models.PROTECT,
        related_name='entregas',
        null=True,
        blank=True)
    garantia = models.ForeignKey(
        tpe_m.TicketSoporte,
        on_delete=models.PROTECT,
        related_name='garantias',
        null=True,
        blank=True)
    observaciones = models.TextField(null=True, blank=True)
    necesita_revision = models.BooleanField(default=True, blank=True, verbose_name='Necesita revisión')
    beneficiario = models.ForeignKey(
        crm_m.Donante,
        on_delete=models.PROTECT,
        related_name='beneficiario',
        null=True,
        blank=True)
    estado = models.ForeignKey(SalidaEstado, on_delete=models.PROTECT, related_name='estados',  null=True, blank=True)
    reasignado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reasignar', null=True, blank=True)

    class Meta:
        verbose_name = "Salida"
        verbose_name_plural = "Salidas"

    def get_absolute_url(self):
        return reverse_lazy('salidainventario_edit', kwargs={'pk': self.id})

    def __str__(self):
        return str(self.id)

    def crear_paquetes(self, cantidad, usuario, entrada, tipo_paquete=None):
        creados = 0
        indice_actual = self.paquetes.count()
        if entrada.count() == 0:
            paquete = Paquete(
                salida=self,
                indice=(1 + indice_actual),
                creado_por=usuario,
                cantidad=cantidad,
                tipo_paquete=tipo_paquete,
            )
            paquete.save()
        else:
            paquete = Paquete(
                salida=self,
                indice=(1 + indice_actual),
                creado_por=usuario,
                cantidad=cantidad,
                tipo_paquete=tipo_paquete,
                )
            paquete.save()
            for numero in entrada:
                paquete.entrada.add(numero)
        creados += 1
        return creados


class SalidaComentario(models.Model):
    salida = models.ForeignKey(SalidaInventario, on_delete=models.CASCADE, related_name='comentarios')
    comentario = models.TextField()
    fecha_revision = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Comentario de revisión de salida'
        verbose_name_plural = 'Comentarios de revisión de salida'

    def __str__(self):
        return '{}'.format(self.comentario[15:])


class PaqueteTipo(models.Model):
    """Tipos de :class:`Paquete` a entregar. Puede incluir las partes básicas de una computadora, como CPU, Teclado,
    etc. o tipos más específicos como componentes de red
    """
    nombre = models.CharField(max_length=35, verbose_name='Nombre del tipo')
    tipo_dispositivo = models.ForeignKey(DispositivoTipo, verbose_name='Tipos de dispositivo', null=True, blank=True)

    class Meta:
        verbose_name = "Tipo de paquete"
        verbose_name_plural = "Tipos de paquete"

    def __str__(self):
        return self.nombre


class Paquete(models.Model):
    """Un conjunto de :class:`Dispositivo` que se descargan del inventario.
    Por default, debería ser una computadora que contenga Mouse, Monitor, CPU, etc.
    Puede ser cualquier otro tipo de paquetes de dispositivos. Por ejemplo, un servidor
    puede tener además de los dipositivos básicos, un dispositivo de red."""
    salida = models.ForeignKey(SalidaInventario, on_delete=models.PROTECT, related_name="paquetes")
    fecha_creacion = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    indice = models.PositiveIntegerField()
    cantidad = models.PositiveIntegerField(default=0)
    tipo_paquete = models.ForeignKey(
        PaqueteTipo,
        on_delete=models.PROTECT,
        related_name='paquetes',
        null=True,
        blank=True)
    aprobado = models.BooleanField(default=False, blank=True)
    aprobado_kardex = models.BooleanField(default=False, blank=True)
    desactivado = models.BooleanField(default=False, blank=True)
    entrada = models.ManyToManyField(Entrada, related_name='tipo_entrada', blank=True, null=True)

    class Meta:
        verbose_name = "Paquete de salida"
        verbose_name_plural = "Paquetes de salida"
        unique_together = ('salida', 'indice')

    def __str__(self):
        return 'P{salida}-{indice}'.format(salida=self.salida, indice=self.indice)

    def aprobar(self, usuario):
        for paquete in self.asignacion.all():
            paquete.aprobado = True
            paquete.aprobado_por = usuario
            paquete.save()

    def get_absolute_url(self):
        return reverse_lazy('detalle_paquete', kwargs={'pk': self.id})

    def asignar_dispositivo(self, lista_dispositivos, usuario):
        """Asigna los dispositivo a los diferentes paquetes que se han creado
        """
        if not self.aprobado:
            for dispositivos in lista_dispositivos:
                if dispositivos.tipo == self.tipo_paquete.tipo_dispositivo:
                    asignar = DispositivoPaquete(
                        dispositivo=dispositivos,
                        paquete=self,
                        asignado_por=usuario
                    )
                    asignar.save()
                else:
                    raise OperationalError('El paquete ya fue aprobado')


class DispositivoPaquete(models.Model):
    """La asignación de un :class:`Dispositivo` a un :class:`Paquete`. Sirve para ser utilizado en control de calidad.
    Cada dispositivo de un paquete debe ser aprobado por control de calidad."""
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.PROTECT, related_name='asignacion')
    paquete = models.ForeignKey(Paquete, on_delete=models.PROTECT, related_name='asignacion')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    asignado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='paquetes_asignados')
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    aprobado = models.BooleanField(default=False)
    aprobado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='paquetes_aprobados')

    class Meta:
        verbose_name = "Asignación Dispositivo - Paquete"
        verbose_name_plural = "Asignaciones Dispositivo - Paquete"

    def __str__(self):
        return '{paquete} -> {dispositivo}'.format(
            paquete=self.paquete,
            dispositivo=self.dispositivo)


class RevisionSalida(models.Model):
    salida = models.ForeignKey(SalidaInventario, on_delete=models.PROTECT, related_name='revisiones')
    revisado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_revision = models.DateTimeField(default=timezone.now, verbose_name='Fecha de revisión')
    anotaciones = models.TextField(null=True, blank=True, verbose_name='Anotaciones generales')
    aprobada = models.BooleanField(default=False, blank=True)
    tecnico = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='tecnicos'
        )

    class Meta:
        verbose_name = 'Revisión de salida'
        verbose_name_plural = 'Revisiones de salida'

    def __str__(self):
        return str(self.salida)

    def get_absolute_url(self):
        return reverse_lazy('revisionsalida_update', kwargs={'pk': self.id})


class RevisionComentario(models.Model):
    revision = models.ForeignKey(RevisionSalida, on_delete=models.CASCADE, related_name='comentarios')
    comentario = models.TextField()
    fecha_revision = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Comentario de revisión'
        verbose_name_plural = 'Comentarios de revisión'

    def __str__(self):
        return '{}'.format(self.comentario[15:])


class SolicitudMovimiento(models.Model):
    """Solicitud de un técnico de área para cambiar cierta cantidad de dispositivos de la etapa. Por ejemplo:
    Un técnico solicitua cambiar 5 monitores de 'Almacenaje en bodega' a 'Tránsito'"""

    etapa_inicial = models.ForeignKey(DispositivoEtapa, on_delete=models.PROTECT, related_name='solicitudes_inicial')
    etapa_final = models.ForeignKey(DispositivoEtapa, on_delete=models.PROTECT, related_name='solicitudes_final')
    fecha_creacion = models.DateField(default=timezone.now)
    creada_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='solicitudes_movimiento')
    recibida_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='recibida_por', null=True)
    autorizada_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='autorizaciones_movimiento',
        null=True)
    tipo_dispositivo = models.ForeignKey(DispositivoTipo, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    terminada = models.BooleanField(default=False)
    recibida = models.BooleanField(default=False)
    devolucion = models.BooleanField(default=False)
    rechazar = models.BooleanField(default=False)
    desecho = models.BooleanField(default=False)
    salida_kardex = models.ForeignKey(
        'kardex.Salida',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='salida_kardex')
    entrada_kardex = models.ForeignKey(
        'kardex.Entrada',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='entrada_kardex')

    class Meta:
        verbose_name = 'Solicitud de movimiento'
        verbose_name_plural = 'Solicitudes de movimiento'

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('solicitudmovimiento_detail', kwargs={'pk': self.id})

    def cambiar_etapa(self, lista_dispositivos, usuario):
        """Cambia el campo `etapa` de la lista de dispositivos recibida.
        En caso de que la solicitud ya haya sido terminada, no se puede volver a realizar esta operación.
        En el ciclo for se realiza la validación para no hacer cambios en dispositivos que no sean del tipo de
        que se está solicitando.
        """
        if not self.terminada:
            for dispositivo in lista_dispositivos:
                if dispositivo.tipo == self.tipo_dispositivo:
                    cambio = CambioEtapa(
                        solicitud=self,
                        dispositivo=dispositivo,
                        etapa_inicial=self.etapa_inicial,
                        etapa_final=self.etapa_final,
                        creado_por=usuario
                    )
                    cambio.save()
            self.terminada = True
            self.save()
        else:
            raise OperationalError('La solicitud ya fue terminada')


class CambioEtapa(models.Model):
    """Registra un movimiento de cambio de etapa en un :class:`Dispositivo`"""
    solicitud = models.ForeignKey(SolicitudMovimiento, on_delete=models.PROTECT, related_name='cambios')
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.PROTECT, related_name='cambios_etapa')
    etapa_inicial = models.ForeignKey(DispositivoEtapa, models.PROTECT, related_name='cambios_inicio')
    etapa_final = models.ForeignKey(DispositivoEtapa, models.PROTECT, related_name='cambios_final')
    fechahora = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Cambio de etapa'
        verbose_name_plural = 'Cambios de etapa'

    def __str__(self):
        return '{dispositivo} -> {final}'.format(
            dispositivo=self.dispositivo,
            final=self.etapa_final)

    def save(self, *args, **kwargs):
        if self.etapa_inicial != self.etapa_final:
            super(CambioEtapa, self).save(*args, **kwargs)
            self.dispositivo.etapa = self.etapa_final
            if self.solicitud.desecho:
                estado_desecho = DispositivoEstado.objects.get(pk=DispositivoEstado.DS)
                self.dispositivo.estado = estado_desecho
            self.dispositivo.save()


class AsignacionTecnico(models.Model):
    """Registra qué dispositivos puede manipular un técnico"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='tipos_dispositivos')
    tipos = models.ManyToManyField(DispositivoTipo, related_name='tipos_disponibles', blank=True)

    class Meta:
        verbose_name = 'Asignacion de técnico'
        verbose_name_plural = 'Asignaciones de técnicos'

    def __str__(self):
        return str(self.usuario)

    def get_absolute_url(self):
        return reverse_lazy('asignaciontecnico_update', kwargs={'pk': self.id})


class CambioEstado(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='cambios_estado')
    estado = models.ForeignKey(DispositivoEstado, on_delete=models.PROTECT, related_name='cambios')
    fecha_hora = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Cambio de estado'
        verbose_name_plural = 'Cambios de estado'

    def __str__(self):
        return '{} -> {}'.format(self.dispositivo, self.estado)

    def save(self, **kwargs):
        super(CambioEstado, self).save(**kwargs)
        self.dispositivo.estado = self.estado
        self.dispositivo.save()


class PrestamoTipo(models.Model):

    """Para indicar el tipo de :class:`Entrada`.
    El campo `contable` indica que los detalles de entrada deben asignar precio.
    """

    nombre = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Tipo de Prestamo"
        verbose_name_plural = "Tipos de Prestamo"

    def __str__(self):
        return self.nombre


class Prestamo(models.Model):
    dispositivo = models.ManyToManyField(Dispositivo, related_name='prestamos')
    tipo_dispositivo = models.ForeignKey(
        DispositivoTipo,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='prestamo_dispositivo')
    tipo_prestamo = models.ForeignKey(
        PrestamoTipo,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='prestamo_tipo')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    fecha_estimada = models.DateField(null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos_creados')
    prestado_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos')
    devuelto = models.BooleanField(default=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'

    def __str__(self):
        return '{} - {}'.format(self.fecha_inicio, self.id)
