from django.db import models
from django.utils import timezone
from django.urls import reverse, reverse_lazy

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

class EscuelaCooperanteManager(models.Manager):
	def get_queryset(self):
		return super(EscuelaCooperanteManager, self).get_queryset().filter(activa=True)

class EscuelaCooperante(models.Model):
	"""
	Description: Asignación de cooperante a escuela
	"""
	escuela = models.ForeignKey('escuela.Escuela', related_name='asignacion_cooperante')
	cooperante = models.ForeignKey(Cooperante, related_name='escuela_asignada')
	activa = models.BooleanField(default=True)
	fecha_activacion = models.DateField(null=True, blank=True, default=timezone.now)
	fecha_anulacion = models.DateField(null=True, blank=True)

	objects = models.Manager()
	activas = EscuelaCooperanteManager()

	def __str__(self):
		return str(self.cooperante) + " - " + str(self.escuela)

		
class EscuelaProyecto(models.Model):
	"""
	Description: Asignación de proyecto a escuela
	"""
	escuela = models.ForeignKey('escuela.Escuela', related_name='asignacion_proyecto')
	proyecto = models.ForeignKey(Proyecto, related_name='escuela_asignada')
	activa = models.BooleanField(default=True)
	fecha_activacion = models.DateField(null=True, blank=True, default=timezone.now)
	fecha_anulacion = models.DateField(null=True, blank=True)

	def __str__(self):
		return str(self.proyecto) + " - " + str(self.escuela)

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
	requisito = models.ManyToManyField(Requisito)

	class Meta:
		verbose_name = 'Versión de solicitud'
		verbose_name_plural = 'Versiones de solicitud'

	def __str__(self):
		return self.nombre