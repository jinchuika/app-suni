from django.db import models
from apps.main.models import Municipio

class EscArea(models.Model):
	area = models.CharField(max_length=20)

	class Meta:
		verbose_name = 'Área'
		verbose_name_plural = 'Áreas'

	def __str__(self):
		return self.area

class EscJornada(models.Model):
	"""
	Description: Jornada de la escuela
	"""
	jornada = models.CharField(max_length=20)

	class Meta:
		verbose_name = 'Jornada'
		verbose_name_plural = 'Jornadas'

	def __str__(self):
		return self.jornada

class EscModalidad(models.Model):
	"""
	Description: Modalidad de la escuela
	"""
	modalidad = models.CharField(max_length=20)

	class Meta:
		verbose_name = 'Modalidad'
		verbose_name_plural = 'Modalidades'

	def __str__(self):
		return self.modalidad


class EscNivel(models.Model):
	"""
	Description: Nivel de la escuela
	"""
	nivel = models.CharField(max_length=30)

	class Meta:
		verbose_name = 'Nivel'
		verbose_name_plural = 'Niveles'

	def __str__(self):
		return self.nivel

class EscPlan(models.Model):
	"""
	Description: Plan de la escuela (diario, fin de semana, etc.)
	"""
	plan = models.CharField(max_length=20)

	class Meta:
		verbose_name = 'Plan'
		verbose_name_plural = 'Planes'

	def __str__(self):
		return self.plan

class EscSector(models.Model):
	"""
	Description: Sector de la escuela (oficial, privado, etc.)
	"""
	sector = models.CharField(max_length=20)

	class Meta:
		verbose_name = 'Sector'
		verbose_name_plural = 'Sectores'

	def __str__(self):
		return self.sector

class EscSatus(models.Model):
	"""
	Description: Status de la escuela (Abierta, cerrada)
	"""
	status = models.CharField(max_length=25)

	class Meta:
		verbose_name = 'Stat'
		verbose_name_plural = 'Statues'

	def __str__(self):
		return self.status

class Escuela(models.Model):
	"""
	Description: Escuela
	"""
	codigo = models.CharField(max_length=15, unique=True)
	distrito = models.CharField(max_length=10)
	municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
	nombre = models.CharField(max_length=250)
	direccion = models.TextField()
	telefono = models.CharField(max_length=12, null=True, blank=True)
	nivel = models.ForeignKey(EscNivel, on_delete=models.PROTECT)
	sector = models.ForeignKey(EscSector, on_delete=models.PROTECT)
	area = models.ForeignKey(EscArea, on_delete=models.PROTECT)
	status = models.ForeignKey(EscSatus, on_delete=models.PROTECT)
	modalidad = models.ForeignKey(EscModalidad, on_delete=models.PROTECT)
	jornada = models.ForeignKey(EscJornada, on_delete=models.PROTECT)
	plan = models.ForeignKey(EscPlan, on_delete=models.PROTECT)

	def __str__(self):
		return self.nombre
