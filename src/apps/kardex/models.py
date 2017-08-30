from __future__ import unicode_literals
from apps.users.models import Perfil
from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy


class Equipo(models.Model):
    nombre = models.CharField(max_length=70)

    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipo'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('kardex_equipo_list')

    @property
    def cantidad_entrada(self):
        return sum(entrada.cantidad for entrada in self.entradas.all())

    @property
    def cantidad_salida(self):
        return sum(detalle.cantidad for detalle in self.detalles_salida.all())

    @property
    def existencia(self):
        return self.cantidad_entrada - self.cantidad_salida


class TipoProveedor(models.Model):
    tipo = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'Tipo de Proveedor'
        verbose_name_plural = 'Tipos de Proveedore'

    def __str__(self):
        return self.tipo


class EstadoEquipo(models.Model):
    estado = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Estado del equipo'
        verbose_name_plural = 'Estados del equipo'

    def __str__(self):
        return self.estado


class TipoSalida(models.Model):
    tipo = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Tipo de salida'
        verbose_name_plural = 'Tipos de salida'

    def __str__(self):
        return self.tipo


class TipoEntrada(models.Model):
    tipo = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Tipo de entrada'
        verbose_name_plural = 'Tipos de entrada'

    def __str__(self):
        return self.tipo


class Proveedor(models.Model):
    nombre = models.CharField(max_length=75)
    tipo = models.ForeignKey(TipoProveedor, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=50, null=True, blank=True, verbose_name='Dirección')
    telefono = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('kardex_proveedor_detail', kwargs={'pk': self.id})

    @property
    def equipo_ingresado(self):
        return sum(entrada.cantidad for entrada in self.entradas.all())


class Entrada(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.PROTECT, related_name='entradas')
    estado = models.ForeignKey(EstadoEquipo, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='entradas')
    tipo = models.ForeignKey(TipoEntrada, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateField()
    precio = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    factura = models.IntegerField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return '{} ({})'.format(self.id, self.fecha)


class Salida(models.Model):
    tecnico = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    fecha = models.DateField()
    tipo = models.ForeignKey(TipoSalida, on_delete=models.PROTECT)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    terminada = models.BooleanField(blank=True, default=False)

    class Meta:
        verbose_name = 'Salida'
        verbose_name_plural = 'Salidas'

    def __str__(self):
        return '{} ({})'.format(self.id, self.fecha)


class SalidaDetalle(models.Model):
    salida = models.ForeignKey(Salida, related_name='detalles', null=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.PROTECT, related_name='detalles_salida')
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return '{} - {}'.format(self.cantidad, self.equipo)
