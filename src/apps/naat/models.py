from django.db import models
from django.contrib.auth.models import User

from apps.cyd.models import Participante


class AsignacionNaat(models.Model):
    participante = models.ForeignKey(Participante, related_name='asignaciones_naat')
    capacitador = models.ForeignKey(User, related_name='asignados_naat')
    fecha_asignacion = models.DateField()
    fecha_finalizacion = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Asignación Naat"
        verbose_name_plural = "Asignaciones Naat"

    def __str__(self):
        return '{} - {}'.format(self.capacitador, self.participante)

    def get_absolute_url(self):
        return ('')
