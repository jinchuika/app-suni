from django.core.exceptions import ValidationError

from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from apps.inventario.models import Entrada as EntradaInventario
from apps.inventario.models import SolicitudMovimiento as SolicitudMovimiento


class Equipo(models.Model):
    nombre = models.CharField(max_length=70)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipo'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('kardex_equipo_list')

    def cantidad_entrada(self):
        return self.detalles_entrada.count()

    def cantidad_salida(self):
        return self.detalles_salida.count()

    def inventario_entrada(self, **kwargs):
        """Obtiene la cantidad de equipo ingresado al inventario

        Args:
            **kwargs: `fecha_inicio` o `fecha_fin`

        Returns:
            TYPE: int
        """
        queryset = self.detalles_entrada.all()
        if 'fecha_inicio' in kwargs and kwargs['fecha_inicio'] is not None:
            queryset = queryset.filter(entrada__fecha__gte=kwargs['fecha_inicio'])
        if 'fecha_fin' in kwargs and kwargs['fecha_fin'] is not None:
            queryset = queryset.filter(entrada__fecha__lte=kwargs['fecha_fin'])
        return sum(detalle.cantidad for detalle in queryset)

    def inventario_salida(self, **kwargs):
        """Obtiene la cantidad de equipo que ha salido del inventario

        Args:
            **kwargs: `fecha_inicio` o `fecha_fin`

        Returns:
            TYPE: int
        """
        queryset = self.detalles_salida.all()
        if 'fecha_inicio' in kwargs and kwargs['fecha_inicio'] is not None:
            queryset = queryset.filter(salida__fecha__gte=kwargs['fecha_inicio'])
        if 'fecha_fin' in kwargs and kwargs['fecha_fin'] is not None:
            queryset = queryset.filter(salida__fecha__lte=kwargs['fecha_fin'])
        return sum(detalle.cantidad for detalle in queryset)

    @property
    def existencia(self):
        return self.inventario_entrada() - self.inventario_salida()


class TipoProveedor(models.Model):
    tipo = models.CharField(max_length=15)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = 'Tipo de Proveedor'
        verbose_name_plural = 'Tipos de Proveedore'

    def __str__(self):
        return self.tipo


class EstadoEquipo(models.Model):
    estado = models.CharField(max_length=10)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = 'Estado del equipo'
        verbose_name_plural = 'Estados del equipo'

    def __str__(self):
        return self.estado


class TipoSalida(models.Model):
    tipo = models.CharField(max_length=25)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = 'Tipo de salida'
        verbose_name_plural = 'Tipos de salida'

    def __str__(self):
        return self.tipo


class TipoEntrada(models.Model):
    tipo = models.CharField(max_length=25)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = 'Tipo de entrada'
        verbose_name_plural = 'Tipos de entrada'

    def __str__(self):
        return self.tipo


class Proveedor(models.Model):
    nombre = models.CharField(max_length=75)
    tipo = models.ForeignKey(TipoProveedor, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=128, null=True, blank=True, verbose_name='Dirección')
    telefono = models.IntegerField(null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('kardex_proveedor_detail', kwargs={'pk': self.id})

    @property
    def equipo_ingresado(self):
        return sum(entrada.cantidad_total for entrada in self.entradas.all())


class Entrada(models.Model):
    estado = models.ForeignKey(EstadoEquipo, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='entradas')
    tipo = models.ForeignKey(TipoEntrada, on_delete=models.PROTECT)
    fecha = models.DateField()
    factura = models.BigIntegerField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    terminada = models.BooleanField(blank=True, default=False)
    inventario_entrada = models.ForeignKey(
        EntradaInventario,
        on_delete=models.PROTECT,
        related_name='inventario',
        null=True,
        blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return '{} ({})'.format(self.id, self.fecha)

    def get_absolute_url(self):
        return reverse_lazy('kardex_entrada_detail', kwargs={'pk': self.id})

    def get_print_url(self):
        """Para generar la URL de la vista de impresión de este modelo.
        """
        return reverse_lazy('kardex_entrada_print', kwargs={'pk': self.id})

    @property
    def precio_total(self):
        return sum(d.precio_total for d in self.detalles.all())

    @property
    def cantidad_total(self):
        return sum(d.cantidad for d in self.detalles.all())


class EntradaDetalle(models.Model):
    entrada = models.ForeignKey(Entrada, related_name='detalles', on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, related_name='detalles_entrada', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0.0)
    class Meta:
        verbose_name = 'Detalle de entrada'
        verbose_name_plural = 'Detalles de entrada'
        # unique_together = ('entrada', 'equipo')

    def __str__(self):
        return '{} - {}'.format(self.entrada, self.equipo)

    def get_absolute_url(self):
        return self.entrada.get_absolute_url()

    @property
    def precio_total(self):
        return self.cantidad * self.precio


class Salida(models.Model):
    tecnico = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha = models.DateField()
    tipo = models.ForeignKey(TipoSalida, on_delete=models.PROTECT)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    terminada = models.BooleanField(blank=True, default=False)
    inventario_movimiento = models.ForeignKey(
        SolicitudMovimiento,
        on_delete=models.PROTECT,
        related_name='movimiento_salida',
        null=True,
        blank=True)

    class Meta:
        verbose_name = 'Salida'
        verbose_name_plural = 'Salidas'

    def __str__(self):
        return '{} ({})'.format(self.id, self.fecha)

    def get_absolute_url(self):
        return reverse_lazy('kardex_salida_detail', kwargs={'pk': self.id})

    def get_print_url(self):
        return reverse_lazy('kardex_salida_print', kwargs={'pk': self.id})


class SalidaDetalle(models.Model):
    salida = models.ForeignKey(Salida, related_name='detalles', null=True, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.PROTECT, related_name='detalles_salida')
    cantidad = models.PositiveIntegerField()
    class Meta:
        verbose_name = 'Detalle de salida'
        verbose_name_plural = 'Detalles de salida'
        unique_together = ('salida', 'equipo')

    def __str__(self):
        return '{} - {}'.format(self.salida, self.equipo)

    def get_absolute_url(self):
        return self.salida.get_absolute_url()

    def clean(self):
        """Para evitar que se retiren más de la existencia actual

        Raises:
            ValidationError: La cantidad no puede ser mayor a la existencia.
        """
        if self.cantidad > self.equipo.existencia:
            raise ValidationError({'cantidad': 'La cantidad no puede ser mayor a la existencia.'})
