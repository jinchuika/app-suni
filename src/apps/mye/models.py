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


class EscuelaCooperante(models.Model):
	"""
	Description: Asignación de cooperante a escuela
	"""
	escuela = models.ForeignKey('escuela.Escuela', related_name='asignacion_cooperante')
	cooperante = models.ForeignKey(Cooperante, related_name='escuela_equipada')
	activa = models.BooleanField(default=True)
	fecha_activacion = models.DateField(null=True, blank=True, default=timezone.now)
	fecha_anulacion = models.DateField(null=True, blank=True)