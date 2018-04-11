from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User

from apps.cyd import models as cyd_m
from apps.escuela import models as escuela_m


class ProcesoNaat(models.Model):
    """Cohorte de un proceso de facilitación de Naat.
    Por este medio se asigna una :class:`Escuela` a un :class:`User` del grupo `naat_facilitador`.
    """
    capacitador = models.ForeignKey(User, related_name='procesos_naat', on_delete=models.CASCADE)
    escuela = models.ForeignKey(escuela_m.Escuela, related_name='procesos_naat', on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Proceso de Naat'
        verbose_name_plural = 'Procesos de Naat'

    def __str__(self):
        return '{escuela} - ({facilitador})'.format(
            escuela=self.escuela,
            facilitador=self.capacitador.get_full_name())

    def get_absolute_url(self):
        return reverse_lazy('proceso_naat_detail', kwargs={'pk': self.id})


class AsignacionNaat(models.Model):
    """
    Asignación de un :class:`Participante` a un facilitador de Naat.
    La asignación a un :class:`Proceso` es opcional
    """
    participante = models.ForeignKey(cyd_m.Participante, related_name='asignaciones_naat', on_delete=models.CASCADE)
    proceso = models.ForeignKey(ProcesoNaat, related_name='asignaciones', null=True, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(default=timezone.now)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Asignación Naat"
        verbose_name_plural = "Asignaciones Naat"
        unique_together = ('participante', 'proceso',)

    def __str__(self):
        return '{} - {}'.format(self.participante, self.proceso)

    def get_absolute_url(self):
        return ('')


class SesionPresencial(models.Model):
    proceso = models.ForeignKey(ProcesoNaat, related_name='sesiones', null=True, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    observaciones = models.TextField(null=True, blank=True)

    asistentes = models.ManyToManyField(AsignacionNaat, blank=True)

    class Meta:
        verbose_name = "Sesión presencial"
        verbose_name_plural = "Sesiones Presenciales"

    def __str__(self):
        return '{escuela} - {fecha}'.format(
            escuela=self.proceso,
            fecha=self.fecha)

    def get_absolute_url(self):
        return reverse_lazy('sesion_naat_detail', kwargs={'pk': self.pk})
