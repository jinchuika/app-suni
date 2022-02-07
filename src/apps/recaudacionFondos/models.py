from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from apps.inventario import models as inv_m
from django.utils import timezone

# Create your models here.

class Proveedor(models.Model):
    """ Datos que se utilizan para crear el reguistro de  los proveedores a
        ingresar
    """
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150, verbose_name="Correo Electrónico")
    numero = models.PositiveIntegerField(default=0,verbose_name="Número Telefónico")
    direccion = models.CharField(max_length=250)
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return str(self.nombre)



class Categoria(models.Model):
    """  Datos de las categorias que se va a crear
    """
    nombre = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return str(self.nombre)

class Articulo(models.Model):
    """Datos que se utilizara para la creacion de los articulos
    """
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Precio sugerido")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural = 'Articulos'

    def __str__(self):
        return str(self.nombre)



class Entrada(models.Model):
    """ Datos que  se utilizaran para la creacion de entradas
    """
    observaciones = models.TextField(null=True, blank=True)
    fecha = models.DateField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    terminada = models.BooleanField(blank=True, default=False)
    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return '{proveedor} -> {id}'.format(
            proveedor=self.proveedor,
            id=self.id)
    def get_absolute_url(self):
        return reverse_lazy('recaudacion_entrada_edit', kwargs={'pk': self.id})



class DetalleEntrada(models.Model):
    """ Detalles que se le asignara a las entradas
    """
    cantidad = models.PositiveIntegerField(default=0)
    caja = models.PositiveIntegerField(default=0)
    entrada = models.ForeignKey(Entrada, related_name='detalles',on_delete=models.PROTECT)
    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT)
    tarima =  models.ForeignKey(inv_m.Tarima, on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'Detalle entrada'
        verbose_name_plural = 'Detalle entradas'

    def __str__(self):
        return '{articulo} -> {entrada}'.format(
            articulo=self.articulo,
            entrada=self.entrada)

    def get_absolute_url(self):
        return reverse_lazy('recaudacion_entrada_edit', kwargs={'pk': self.entrada.id})

class TipoSalida(models.Model):
    """ Nombre del tipo de salida que se va a signar
    """
    nombre = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Tipo salida'
        verbose_name_plural = 'Tipos salidas'

    def __str__(self):
        return str(self.nombre)

class Salida(models.Model):
    """ Datos que se utiliza para la creaciond e salidas
    """
    observaciones = models.TextField(null=True, blank=True)
    fecha = models.DateField()
    url = models.URLField(blank=True)
    tipo = models.ForeignKey(TipoSalida, on_delete=models.PROTECT)
    terminada = models.BooleanField(blank=True, default=False)
    class Meta:
        verbose_name = 'Salida'
        verbose_name_plural = 'Salidas'

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('recaudacion_salida_update', kwargs={'pk': self.id})

class DetalleSalida(models.Model):
    """ Detalle que se le asignara a cada salida
    """
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.PositiveIntegerField(default=0)
    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT)
    salida = models.ForeignKey(Salida,related_name='salida_detalle', on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'Detalle salida'
        verbose_name_plural = 'Detalles salidas'

    def __str__(self):
        return '{articulo} -> {salida}'.format(
            articulo=self.articulo,
            salida=self.salida)

    def get_absolute_url(self):
        return reverse_lazy('recaudacion_salida_update', kwargs={'pk': self.salida})
