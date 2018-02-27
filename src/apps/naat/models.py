from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User

from apps.cyd import models as cyd_m
from apps.escuela import models as escuela_m


class AsignacionNaat(models.Model):
    participante = models.ForeignKey(cyd_m.Participante, related_name='asignaciones_naat')
    capacitador = models.ForeignKey(User, related_name='asignados_naat')
    fecha_asignacion = models.DateField(default=timezone.now)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Asignación Naat"
        verbose_name_plural = "Asignaciones Naat"
        unique_together = ('participante', 'capacitador', 'activa',)

    def __str__(self):
        return '{} - {}'.format(self.capacitador, self.participante)

    def get_absolute_url(self):
        return ('')


class SesionPresencial(models.Model):
    escuela = models.ForeignKey(escuela_m.Escuela)
    capacitador = models.ForeignKey(User, related_name='sesiones_naat')
    fecha = models.DateField()
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    ovservaciones = models.TextField(null=True, blank=True)

    asistentes = models.ManyToManyField(AsignacionNaat, blank=True)

    class Meta:
        verbose_name = "Sesión presencial"
        verbose_name_plural = "Sesiones Presenciales"

    def __str__(self):
        return '{escuela} - {fecha}'.format(
            escuela=self.escuela,
            fecha=self.fecha)

    def get_absolute_url(self):
        return reverse_lazy('sesion_naat_detail', kwargs={'pk': self.pk})
