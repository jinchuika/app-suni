from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from apps.escuela import models as escuela_m


class Cooperante(models.Model):
    """
    Description: Cooperante para equipamiento
    """
    nombre = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse_lazy('cooperante_detail', args=[str(self.id)])

    def __str__(self):
        return self.nombre


class Proyecto(models.Model):
    """
    Description: Proyecto de equipamiento
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('proyecto_detail', args=[str(self.id)])


class Requisito(models.Model):
    """
    Description: Requerimiento de solicitud
    """
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class SolicitudVersion(models.Model):
    """
    Description: Versión de solicitud de equipamiento
    """
    nombre = models.CharField(max_length=50)
    requisito = models.ManyToManyField(Requisito, blank=True)

    class Meta:
        verbose_name = 'Versión de solicitud'
        verbose_name_plural = 'Versiones de solicitud'

    def __str__(self):
        return self.nombre


class Medio(models.Model):
    """
    Description: Medio de comunicación
    """
    medio = models.CharField(max_length=50)

    def __str__(self):
        return self.medio


class Solicitud(models.Model):
    """
    Description: Solicitud de equipamiento
    """
    version = models.ForeignKey(SolicitudVersion, on_delete=models.PROTECT, related_name='solicitud')
    formulario = models.BooleanField(default=False, blank=True)
    escuela = models.ForeignKey(escuela_m.Escuela, on_delete=models.PROTECT, related_name='solicitud')
    fecha = models.DateField()
    jornada = models.IntegerField()
    edf = models.BooleanField(blank=True)
    lab_actual = models.BooleanField(blank=True)

    poblacion = models.ForeignKey(
        escuela_m.EscPoblacion,
        on_delete=models.PROTECT,
        related_name='solicitudes',
        null=True)

    requisito = models.ManyToManyField(Requisito, blank=True)
    medio = models.ManyToManyField(Medio, blank=True)

    observacion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('escuela_solicitud_detail', kwargs={'pk': self.escuela.id, 'id_solicitud': self.id})

    def porcentaje_requisitos(self):
        return self.requisito.count() / self.version.requisito.count() * 100

    def listar_requisito(self):
        queryset_requisito = self.version.requisito.all()
        requisito_list = []
        for requisito in queryset_requisito:
            if requisito in self.requisito.all():
                requisito_list.append({'requisito': requisito, 'cumple': True})
            else:
                requisito_list.append({'requisito': requisito, 'cumple': False})
        return requisito_list


class ValidacionVersion(models.Model):
    nombre = models.CharField(max_length=30)
    requisito = models.ManyToManyField(Requisito, blank=True)

    class Meta:
        verbose_name = "Versión de validación"
        verbose_name_plural = "Versiones de validación"

    def __str__(self):
        return self.nombre


class ValidacionTipo(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Tipo de validación"
        verbose_name_plural = "Tipos de validación"

    def __str__(self):
        return self.nombre


class Validacion(models.Model):
    version = models.ForeignKey(ValidacionVersion)
    tipo = models.ForeignKey(ValidacionTipo)
    escuela = models.ForeignKey('escuela.Escuela', on_delete=models.PROTECT, related_name='validacion')
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_final = models.DateField(null=True, blank=True)
    jornada = models.IntegerField(default=1)
    fecha_equipamiento = models.DateField(null=True, blank=True)
    fotos_link = models.URLField(null=True, blank=True)

    poblacion = models.ForeignKey(
        escuela_m.EscPoblacion,
        on_delete=models.PROTECT,
        related_name='validaciones',
        null=True)

    requisito = models.ManyToManyField(Requisito, blank=True)

    observacion = models.TextField(null=True, blank=True)
    completada = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = "Validacion"
        verbose_name_plural = "Validaciones"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('escuela_validacion_detail', kwargs={'pk': self.escuela.id, 'id_validacion': self.id})

    def porcentaje_requisitos(self):
        return self.requisito.count() / self.version.requisito.count() * 100

    def listar_requisito(self):
        queryset_requisito = self.version.requisito.all()
        requisito_list = []
        for requisito in queryset_requisito:
            if requisito in self.requisito.all():
                requisito_list.append({'requisito': requisito, 'cumple': True})
            else:
                requisito_list.append({'requisito': requisito, 'cumple': False})
        return requisito_list


class ValidacionComentario(models.Model):
    validacion = models.ForeignKey(Validacion, related_name='comentarios')
    comentario = models.TextField()
    usuario = models.ForeignKey(User)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Comentario de validación"
        verbose_name_plural = "Comentarios de validación"

    def __str__(self):
        return str(self.validacion) + self.comentario[:15] + '...'
