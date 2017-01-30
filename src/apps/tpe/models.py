from django.db import models
from django.utils import timezone


class EquipamientoEstado(models.Model):
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.estado


class EquipamientoTipoRed(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo


class Equipamiento(models.Model):
    id = models.IntegerField(primary_key=True)
    estado = models.ForeignKey(
        EquipamientoEstado,
        default=1,
        on_delete=models.PROTECT)
    escuela = models.ForeignKey('escuela.Escuela', related_name='equipamiento')
    fecha = models.DateField(default=timezone.now)
    observacion = models.TextField(null=True, blank=True)
    renovacion = models.BooleanField(blank=True, default=False)
    servidor_khan = models.BooleanField(blank=True, default=False)
    cantidad_equipo = models.IntegerField(default=0)
    red = models.BooleanField(blank=True, default=False)
    tipo_red = models.ForeignKey(EquipamientoTipoRed, null=True, blank=True)
    fotos = models.BooleanField(default=False, blank=True)
    manual = models.BooleanField(default=False, blank=True)
    edulibre = models.BooleanField(default=False, blank=True)
    carta = models.BooleanField(default=False, blank=True)

    cooperante = models.ManyToManyField('mye.Cooperante', blank=True)
    proyecto = models.ManyToManyField('mye.Proyecto', blank=True)

    def __str__(self):
        return str(self.id)
