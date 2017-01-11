from django.db import models


class Curso(models.Model):
    """
    Description: Curso de capacitación
    """
    nombre = models.CharField(max_length=75)
    nota_aprobacion = models.IntegerField()
    porcentaje = models.IntegerField()

    def __str__(self):
        return self.nombre


class CrAsistencia(models.Model):
    """
    Description: Asistencia a curso
    """
    curso = models.ForeignKey(Curso, related_name="asistencia")
    modulo_num = models.IntegerField()
    punteo_max = models.IntegerField()

    class Meta:
        unique_together = ('curso', 'modulo_num',)

    def __str__(self):
        return str(self.modulo_num) + " de " + str(self.curso)


class CrHito(models.Model):
    """
    Description: Hito a curso
    """
    curso = models.ForeignKey(Curso, related_name="hito")
    nombre = models.CharField(max_length=40)
    punteo_max = models.IntegerField()

    def __str__(self):
        return str(self.nombre) + " de " + str(self.curso)
