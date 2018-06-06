from django.db import models
from django.conf import settings


class EscuelaSede(models.Model):

    """Para obtener las sedes de capacitación en las que ha participado
    una escuela.
    """

    id = models.CharField(max_length=20, primary_key=True)
    sede = models.CharField(max_length=125)
    udi = models.CharField(max_length=125)
    escuela = models.CharField(max_length=120)
    inicio = models.DateField()
    fin = models.DateField()
    participantes = models.PositiveIntegerField()
    capacitador = models.CharField(max_length=100)

    class Meta:
        if settings.LEGACY_CONNECTION:
            managed = False
        db_table = 'v_sede_escuela'
        verbose_name = 'Escuela capacitada'
        verbose_name_plural = 'Escuelas capacitadas'

    def __str__(self):
        return '{} - {}'.format(self.sede, self.udi)
