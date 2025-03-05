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
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    def get_absolute_url(self):
        return reverse_lazy('cooperante_detail', args=[str(self.id)])

    def get_mapa_url(self):
        return reverse_lazy('cooperante_mapa', kwargs={'pk': self.id})

    def __str__(self):
        return self.nombre


class Proyecto(models.Model):
    """
    Description: Proyecto de equipamiento
    """
    nombre = models.CharField(max_length=100)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('proyecto_detail', args=[str(self.id)])

    @property
    def cantidad_equipamientos(self):
        return self.equipamientos.count()


class Requisito(models.Model):
    """
    Description: Requerimiento de solicitud
    """
    nombre = models.CharField(max_length=50)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    def __str__(self):
        return self.nombre


class SolicitudVersion(models.Model):
    """
    Description: Versión de solicitud de equipamiento
    """
    nombre = models.CharField(max_length=50)
    requisito = models.ManyToManyField(Requisito, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
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
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
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

    prom_mat_seg_p = models.FloatField(blank=True, null=True, verbose_name='Promedio matemática segundo primaria')
    prom_mat_quinto_p = models.FloatField(blank=True, null=True, verbose_name='Promedio matemática quinto primaria')
    prom_mat_seg_b = models.FloatField(blank=True, null=True, verbose_name='Promedio matemática segundo básico')
    grupos_familia = models.IntegerField(blank=True, null=True, verbose_name='Grupos familias')
    internet = models.BooleanField(default=False, blank=True)
    requisito = models.ManyToManyField(Requisito, blank=True)
    medio = models.ManyToManyField(Medio, blank=True)

    observacion = models.TextField(null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
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
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = "Versión de validación"
        verbose_name_plural = "Versiones de validación"

    def __str__(self):
        return self.nombre


class ValidacionTipo(models.Model):
    nombre = models.CharField(max_length=30)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = "Tipo de validación"
        verbose_name_plural = "Tipos de validación"

    def __str__(self):
        return self.nombre


class Validacion(models.Model):
    version = models.ForeignKey(ValidacionVersion, on_delete=models.CASCADE)
    tipo = models.ForeignKey(ValidacionTipo, on_delete=models.CASCADE)
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

    prom_mat_seg_p = models.FloatField(blank=True, null=True, verbose_name='Promedio matemática segundo primaria')
    prom_mat_quinto_p = models.FloatField(blank=True, null=True, verbose_name='Promedio matemática quinto primaria')
    prom_mat_seg_b = models.FloatField(blank=True, null=True, verbose_name='Promedio matemática segundo básico')
    grupos_familia = models.IntegerField(blank=True, null=True, verbose_name='Grupos familias')
    internet = models.BooleanField(default=False, blank=True)
    requisito = models.ManyToManyField(Requisito, blank=True)

    observacion = models.TextField(null=True, blank=True)
    completada = models.BooleanField(default=False, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,related_name="mye_creada_por",default=User.objects.get(username="Admin").pk)
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
    validacion = models.ForeignKey(Validacion, related_name='comentarios', on_delete=models.CASCADE)
    comentario = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Comentario de validación"
        verbose_name_plural = "Comentarios de validación"

    def __str__(self):
        return str(self.validacion) + self.comentario[:15] + '...'


class SolicitudComentario(models.Model):
    solicitud = models.ForeignKey(Solicitud, related_name='comentarios_solicitud', on_delete=models.CASCADE)
    comentario = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Comentario de Solicitud"
        verbose_name_plural = "Comentarios de Solicitud"

    def __str__(self):
        return str(self.validacion) + self.comentario[:15]+'...'


class UsuarioCooperante(models.Model):
    cooperante = models.ForeignKey(Cooperante, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cooperantes')

    class Meta:
        verbose_name = "Usuario de cooperante"
        verbose_name_plural = "Usuarios de cooperantes"

    def __str__(self):
        return '{} - {}'.format(self.cooperante, self.usuario)

    @property
    def estadistica(self):
        return self.cooperante.equipamientos.aggregate(
            total_alumno=models.Sum(
                'poblacion__total_alumno',
                filter=models.Q(poblacion__isnull=False)),
            total_maestro=models.Sum(
                'poblacion__total_maestro',
                filter=models.Q(poblacion__isnull=False)),
            cantidad_equipo=models.Sum('cantidad_equipo'),
            equipamientos=models.Count('id')
            )
