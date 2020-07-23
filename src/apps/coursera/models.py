from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Aliado(models.Model):
    """Aliados al programa Coursera para Guatemala:
    """
    aliado = models.CharField(max_length=50, verbose_name="Aliado Coursera")

    class Meta:
        verbose_name = "Aliado"
        verbose_name_plural = "Aliados"

    def __str__(self):
        return self.aliado

class Monitoreo(models.Model):
    """Monitoreo de invitaciones vrs. miembros por aliado:
    """
    aliado = models.ForeignKey(Aliado, on_delete=models.PROTECT, related_name='estadísticas')
    fecha = models.DateField(default=timezone.now)
    invitaciones = models.PositiveIntegerField(default=0, verbose_name='Invitaciones Enviadas')
    miembros = models.PositiveIntegerField(default=0, verbose_name='Miembros Registrados')

    class Meta:
        verbose_name = "Monitoreo"
        verbose_name_plural = "Estadísticas de monitoreo"

    def __str__(self):
        return self.aliado

    @property
    def porcentaje(self):
    	porcentaje = ((self.miembros / self.invitaciones))
    	return "{:.2%}".format(porcentaje)