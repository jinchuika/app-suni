from __future__ import unicode_literals
from apps.users.models import Perfil
from django.db import models
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
    estado = models.ForeignKey(EstadoEquipo, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='entradas')
    tipo = models.ForeignKey(TipoEntrada, on_delete=models.PROTECT)
    fecha = models.DateField()
    factura = models.IntegerField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    terminada = models.BooleanField(blank=True, default=False)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return '{} ({})'.format(self.id, self.fecha)

    def get_absolute_url(self):
        return reverse_lazy('kardex_entrada_detail', kwargs={'pk': self.id})

    @property
    def precio_total(self):
        return sum(d.precio for d in self.detalles.all())


class EntradaDetalle(models.Model):
    entrada = models.ForeignKey(Entrada, related_name='detalles')
    equipo = models.ForeignKey(Equipo, related_name='detalles_entrada')
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Detalle de entrada'
        verbose_name_plural = 'Detalles de entrada'

    def __str__(self):
        return '{} - {}'.format(self.entrada, self.equipo)

    def get_absolute_url(self):
        return self.entrada.get_absolute_url()


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
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('kardex_salida_detail', kwargs={'pk': self.id})

    def get_print_url(self):
        return reverse_lazy('kardex_salida_print', kwargs={'pk': self.id})


class SalidaDetalle(models.Model):
    salida = models.ForeignKey(Salida, related_name='detalles', null=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.PROTECT, related_name='detalles_salida')
    cantidad = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Detalle de salida'
        verbose_name_plural = 'Detalles de salida'
        unique_together = ('salida', 'equipo')

    def __str__(self):
        return '{} - {}'.format(self.entrada, self.equipo)

    def get_absolute_url(self):
        return self.salida.get_absolute_url()
