from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from apps.users.models import Organizacion
from apps.escuela.models import Escuela, EscPoblacion


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


class SoftwareItem(models.Model):
    software = models.CharField(max_length=100)
    sistema_operativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Software para equipo"
        verbose_name_plural = "Software para equipo"

    def __str__(self):
        return self.software


class Item(models.Model):

    """Producto a ser entregado en los laboratorios. Es el
    "inventario" de la totalidad del equipo que se puede entregar a
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


class LaboratorioTipo(models.Model):
    tipo = models.CharField(max_length=35)

    class Meta:
        verbose_name = "Tipo de laboratorio"
        verbose_name_plural = "Tipos de laboratorios"

    def __str__(self):
        return self.tipo


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

    escuela = models.ForeignKey(Escuela, related_name='laboratorios', on_delete=models.CASCADE)
    organizacion = models.ForeignKey(
        Organizacion,
        related_name='laboratorios',
        verbose_name='Organización',
        on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    observaciones = models.TextField(null=True, blank=True)
    red = models.BooleanField(default=False, blank=True)
    internet = models.BooleanField(default=False, blank=True)
    fotos_link = models.URLField(null=True, blank=True, verbose_name='Link a fotos (GDrive)')
    marca_equipo = models.ForeignKey(
        MarcaItem,
        related_name='laboratorios',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    tipo_equipo = models.ForeignKey(
        TipoItem,
        related_name='laboratorios',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Tipo de equipo')
    equipo_uniforme = models.BooleanField(default=True, blank=True, verbose_name='El equipo es uniforme')
    servidor_local = models.BooleanField(default=False, blank=True, verbose_name='Posee servidor local')
    poblacion = models.ForeignKey(
        EscPoblacion,
        related_name='laboratorios',
        verbose_name='Población',
        on_delete=models.CASCADE)
    cantidad_computadoras = models.PositiveIntegerField(default=0, verbose_name='Cantidad de computadoras')

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('laboratorio_detail', kwargs={'pk': self.id})


class Computadora(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, related_name='computadoras', on_delete=models.CASCADE)
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
    computadora = models.ForeignKey(Computadora, related_name='series', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Serie"
        verbose_name_plural = "Series"

    def __str__(self):
        return '{computadora}-{item}'.format(
            item=self.item.id,
            computadora=self.computadora.id)

    def get_absolute_url(self):
        return self.computadora.get_absolute_url()


class Requerimiento(models.Model):
    """
    Description: Requerimiento para equipamiento
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class ValidacionVersion(models.Model):
    nombre = models.CharField(max_length=50)
    activa = models.BooleanField(default=True, blank=True)
    requisitos = models.ManyToManyField(Requerimiento, blank=True)

    class Meta:
        verbose_name = "Versión de validación"
        verbose_name_plural = "Versiones de validaciónes"

    def __str__(self):
        return self.nombre


class Validacion(models.Model):
    escuela = models.ForeignKey(Escuela, related_name='ie_validaciones', on_delete=models.CASCADE)
    version = models.ForeignKey(ValidacionVersion, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now, verbose_name='Fecha de inicio')
    fotos_link = models.URLField(null=True, blank=True, verbose_name='Link a fotos')
    observaciones = models.TextField(null=True, blank=True)
    completada = models.BooleanField(default=False, blank=True)
    fecha_fin = models.DateField(verbose_name='Fecha de fin', null=True, blank=True)
    organizacion = models.ForeignKey(Organizacion, null=True, blank=True, on_delete=models.CASCADE)
    creada_por = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    requerimientos = models.ManyToManyField(Requerimiento, blank=True)

    class Meta:
        verbose_name = "Validacion"
        verbose_name_plural = "Validacions"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('ie_validacion_detail', kwargs={'pk': self.id})

    def porcentaje_requisitos(self):
        return round(
            self.requerimientos.count() / self.version.requisitos.count() * 100,
            2)

    def listar_requerimientos(self):
        req_de_version = self.version.requisitos.all()
        requerimiento_list = []
        for requerimiento in req_de_version:
            requerimiento_list.append(
                {
                    'requerimiento': requerimiento,
                    'cumple': requerimiento in self.requerimientos.all()
                })
        return requerimiento_list
