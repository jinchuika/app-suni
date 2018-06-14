#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class PeriodoFiscal(models.Model):
    """Periodo en el cual se pueden contar movimientos de inventario y de repuestos. Sirve para agrupar
    los precios movimientos y que cada dispositivo tenga únicamente un precio en un periodo contable."""

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    actual = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = 'Periodo fiscal'
        verbose_name_plural = 'Periodos fiscales'

    def __str__(self):
        return '{} - {}'.format(self.fecha_inicio, self.fecha_fin)


class PrecioEstandar(models.Model):
    """Precio por defecto a asignar a un dispositivo o repuesto que ingrese sin específicar un precio, tomando
    como punto de partida su tipo. Un tipo únicamente puede tener un precio estándar en el mismo periodo.
    """

    DISPOSITIVO = 'dispositivo'
    REPUESTO = 'repuesto'

    INVENTARIO_CHOICES = (
        (DISPOSITIVO, 'Dispositivo'),
        (REPUESTO, 'Repuesto')
    )

    periodo = models.ForeignKey(PeriodoFiscal, on_delete=models.CASCADE, related_name='precios')
    tipo_dispositivo = models.ForeignKey('inventario.DispositivoTipo', on_delete=models.CASCADE, related_name='precios')
    activo = models.BooleanField(default=True, blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    inventario = models.CharField(max_length=12, choices=INVENTARIO_CHOICES, default=DISPOSITIVO)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('periodo', 'tipo_dispositivo')
        verbose_name = 'Precio estándar'
        verbose_name_plural = 'Precios estándar'
        indexes = [
            models.Index(fields=['inventario', ])
        ]

    def __str__(self):
        return '{} - {}'.format(self.periodo, self.tipo_dispositivo)


class PrecioDispositivo(models.Model):
    """Precio asignado a un :clas:`Dispositivo` en un :class:`PeriodoFiscal`. Estos datos NO se pueden
    repetir, ya que un dispositivo no puede cambiar de precio en el mismo período
    """

    dispositivo = models.ForeignKey('inventario.Dispositivo', on_delete=models.CASCADE, related_name='precios')
    precio = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    periodo = models.ForeignKey(PeriodoFiscal, on_delete=models.CASCADE, related_name='precios_dispositivo')
    activo = models.BooleanField(default=True, blank=True)
    fecha_creacion = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Precio de dispositivo'
        verbose_name_plural = 'Precios de dispositivos'
        unique_together = ('dispositivo', 'periodo')

    def __str__(self):
        return '{dispositivo} - Q{precio}'.format(dispositivo=self.dispositivo, precio=self.precio)


class PrecioRepuesto(models.Model):
    """Precio asignado a un :clas:`Repuesto` en un :class:`PeriodoFiscal`. Estos datos NO se pueden
    repetir, ya que un repuesto no puede cambiar de precio en el mismo período
    """
    repuesto = models.ForeignKey('inventario.Repuesto', on_delete=models.CASCADE, related_name='precios')
    precio = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    periodo = models.ForeignKey(PeriodoFiscal, on_delete=models.CASCADE, related_name='precios_repuesto')
    activo = models.BooleanField(default=True, blank=True)
    fecha_creacion = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Precio de repuesto'
        verbose_name_plural = 'Precios de repuestos'
        unique_together = ('repuesto', 'periodo')

    def __str__(self):
        return '{dispositivo} - Q{precio}'.format(dispositivo=self.repuesto, precio=self.precio)


class MovimientoDispositivo(models.Model):
    """Transacción que indica altas o bajas de dispositivos en el inventario.
    La cantidad de existencias de un tipo de dispositivos se calcula sumando el campo `tipo_movimiento`, que tendrá los
    valores de `-1` o `1` para bajas y altas, respectivamente.
    """

    BAJA = -1
    ALTA = 1
    TIPO_CHOICES = (
        (BAJA, 'Baja'),
        (ALTA, 'Alta')
    )

    fecha = models.DateField(default=timezone.now)
    dispositivo = models.ForeignKey('inventario.Dispositivo')
    periodo_fiscal = models.ForeignKey(PeriodoFiscal, on_delete=models.PROTECT, related_name='movimientos_dispositivo')
    tipo_movimiento = models.IntegerField(choices=TIPO_CHOICES, default=ALTA)
    precio = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    referencia = models.CharField(max_length=30, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Movimiento de dispositivo'
        verbose_name_plural = 'Movimientos de dispositivos'
    
    def __str__(self):
        return '{} - {}'.format(self.tipo_movimiento, self.dispositivo)


class MovimientoRepuesto(models.Model):
    """Transacción que indica altas o bajas de repuestos en el inventario.
    La cantidad de existencias de un tipo de dispositivos se calcula sumando el campo `tipo_movimiento`, que tendrá los
    valores de `-1` o `1` para bajas y altas, respectivamente.
    """

    BAJA = -1
    ALTA = 1
    TIPO_CHOICES = (
        (BAJA, 'Baja'),
        (ALTA, 'Alta')
    )

    fecha = models.DateField(default=timezone.now)
    repuesto = models.ForeignKey('inventario.Repuesto')
    periodo_fiscal = models.ForeignKey(PeriodoFiscal, on_delete=models.PROTECT, related_name='movimientos_repuesto')
    tipo_movimiento = models.IntegerField(choices=TIPO_CHOICES, default=ALTA)
    precio = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    referencia = models.CharField(max_length=30, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Movimiento de repuesto'
        verbose_name_plural = 'Movimientos de repuestos'

    def __str__(self):
        return '{} - {}'.format(self.tipo_movimiento, self.repuesto)
