from django.db import models
from apps.users.models import Perfil
from django.contrib.auth.models import Group

class Departamento(models.Model):
	"""
	Description: Departamento de Guatemala
	"""
	nombre = models.CharField(max_length=30)

	def __str__(self):
		return self.nombre


class Municipio(models.Model):
	"""
	Description: Municipio de Guatemala
	"""
	departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
	nombre = models.CharField(max_length=150)

	def __str__(self):
		return self.nombre + " ("+ str(self.departamento) + ")"
