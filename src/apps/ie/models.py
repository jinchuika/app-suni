from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy

from apps.users.models import Organizacion
from apps.escuela.models import Escuela, EscPoblacion


class Laboratorio(models.Model):

    """Laboratorio entregado a una escuela.

    Attributes:
        escuela (:class:`Escuela`): Escuela que recibe el equipamiento
        fecha (date): Fecha en la que se realiza la entrega del equipo
        fotos_link (str): Link hacia carpeta de Google Drive
        internet (bool): Indica si la escuela tiene conexión a internet
        observaciones (str): Observaciones generales del equipamiento
        organizacion (:class:`Organizacion`): Entidad que realiza la entrega
        red (bool): Indica si la escuela tiene red de área local
    """

    escuela = models.ForeignKey(Escuela)
    organizacion = models.ForeignKey(Organizacion, related_name='laboratorios', verbose_name='Organización')
    fecha = models.DateField(default=timezone.now)
    observaciones = models.TextField(null=True, blank=True)
    red = models.BooleanField(default=False, blank=True)
    internet = models.BooleanField(default=False, blank=True)
    fotos_link = models.URLField(null=True, blank=True)
    poblacion = models.ForeignKey(EscPoblacion, related_name='laboratorios', verbose_name='Población')

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('laboratorio_detail', kwargs={'pk': self.id})


class TipoItem(models.Model):

    """Tipo de item que se puede entregar (Monitor, teclado, etc.)

    Attributes:
        tipo (str): Nombre del tipo de equipo
    """

    tipo = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Tipo de Item"
        verbose_name_plural = "Tipos de Items"

    def __str__(self):
        return self.tipo


class MarcaItem(models.Model):
    """Marca de item que se puede entregar

    Attributes:
        marca (str): Nombre de la marca del equipo
    """
    marca = models.CharField(max_length=35)

    class Meta:
        verbose_name = "Marca de item"
        verbose_name_plural = "Marcas de items"

    def __str__(self):
        return self.marca


class Item(models.Model):

    """Producto a ser entregado en los laboratorios. Es el
    "inventario" de todo el equipo que se puede entregar a
    las escuelas.

    Attributes:
        tipo (:class:`TipoItem`): El tipo de producto que se puede entregar
        marca (:class:`MarcaItem`): La marca del producto que se puede entregar
        modelo (str): El modelo del producto
    """

    tipo = models.ForeignKey(TipoItem, on_delete=models.PROTECT)
    marca = models.ForeignKey(MarcaItem, on_delete=models.PROTECT)
    modelo = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return '{marca} {modelo}'.format(
            marca=self.marca,
            modelo=self.modelo)


class Computadora(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, related_name='computadoras')
    items = models.ManyToManyField(Item, through='Serie', related_name='computadoras')
    completa = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = "Computadora"
        verbose_name_plural = "Computadoras"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return self.laboratorio.get_absolute_url()


class Serie(models.Model):
    computadora = models.ForeignKey(Computadora, related_name='series')
    item = models.ForeignKey(Item)

    class Meta:
        verbose_name = "Serie"
        verbose_name_plural = "Series"

    def __str__(self):
        return '{computadora}-{item}'.format(
            item=self.item.id,
            computadora=self.computadora.id)

    def get_absolute_url(self):
        return self.computadora.get_absolute_url()
