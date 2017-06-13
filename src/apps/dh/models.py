from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from apps.mye.models import Cooperante


class TipoEvento(models.Model):
    tipo_evento = models.CharField(max_length=25)
    color = models.CharField(max_length=12, default='')

    class Meta:
        verbose_name = "Tipo de evento de Dejando Huella"
        verbose_name_plural = "Tipos de evento de Dejando Huella"

    def __str__(self):
        return self.tipo_evento


class EventoDH(models.Model):
    tipo_evento = models.ForeignKey(TipoEvento, verbose_name="Tipo de evento")
    titulo = models.TextField(verbose_name="Título")
    fecha = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(null=True, blank=True, verbose_name="Hora de inicio")
    hora_fin = models.TimeField(null=True, blank=True, verbose_name="Hora de fin")
    ubicacion = models.TextField(null=True, blank=True, verbose_name="Ubicación")
    creado_por = models.ForeignKey(User, related_name="eventos_dh")
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    asistentes = models.ManyToManyField(User, blank=True)
    cooperantes = models.ManyToManyField(Cooperante, blank=True)

    fotos = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Evento de Dejando Huella"
        verbose_name_plural = "Eventos de Dejando Huella"

    def __str__(self):
        return str(self.titulo)

    def save(self, *args, **kwargs):
        if self.hora_inicio and not self.hora_fin:
            self.hora_fin = self.hora_inicio + timedelta(hours=2)
        super(EventoDH, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('evento_dh_detail', kwargs={'pk': self.id})
