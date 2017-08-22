from django.db import models
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from apps.escuela.models import Escuela


class Visita(models.Model):
    """Visita de seguimiento de KA Lite después de que la escuela ha
    recibido la capacitación.
    """

    escuela = models.ForeignKey(Escuela, related_name='visitas_kalite')
    fecha = models.DateField()
    capacitador = models.ForeignKey(User, related_name='visitas_kalite')

    class Meta:
        verbose_name = "Visita de KA Lite"
        verbose_name_plural = "Visitas de KA Lite"

    def __str__(self):
        return '{} - {}'.format(self.fecha, self.escuela)


class Rubrica(models.Model):
    """Rúbrica de evaluación."""

    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        verbose_name = "Rúbrica"
        verbose_name_plural = "Rúbricas"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('rubrica_detail', kwargs={'pk': self.id})


class Indicador(models.Model):
    """Indicador a evaluar de la :model:`kalite.Rubrica`."""
    rubrica = models.ForeignKey(Rubrica, related_name='indicadores')
    indicador = models.TextField()

    class Meta:
        verbose_name = "Indicador"
        verbose_name_plural = "Indicadors"

    def __str__(self):
        return self.indicador

    def get_absolute_url(self):
        return self.rubrica.get_absolute_url()


class Evaluacion(models.Model):
    """Evaluación realizada durante una :model:`kalite.Visita` en base
    a una :model:`kalite.Rubrica`.
    """

    visita = models.ForeignKey(Visita, related_name='evaluaciones')
    rubrica = models.ForeignKey(Rubrica)

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        unique_together = ('visita', 'rubrica')

    def __str__(self):
        return '{} - {}'.format(self.rubrica, self.visita)


class Punteo(models.Model):
    """Punteo asignado a un :model:`kalite.Indicador` durante
    una :model:`kalite.Evaluacion`.
    """
    NOTA_1 = 1
    NOTA_2 = 2
    NOTA_3 = 3
    NOTA_4 = 4
    NOTA_5 = 5
    NOTA_CHOICES = (
        (NOTA_1, '20%'),
        (NOTA_2, '40%'),
        (NOTA_3, '60%'),
        (NOTA_4, '80%'),
        (NOTA_5, '100%'))

    evaluacion = models.ForeignKey(Evaluacion)
    indicador = models.ForeignKey(Indicador)
    nota = models.IntegerField(choices=NOTA_CHOICES, default=NOTA_1)

    class Meta:
        verbose_name = "Punteo"
        verbose_name_plural = "Punteos"

    def __str__(self):
        return self.nota


class Grado(models.Model):
    """Registro de grado (con sección) durante una :model:`kalite.Visita`."""

    visita = models.ForeignKey(Visita, related_name='grados')
    grado = models.IntegerField()
    seccion = models.CharField(max_length=2, null=True, blank=True, verbose_name='Sección')
    minimo_esperado = models.PositiveIntegerField(verbose_name='Mínimo esperado')

    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
        unique_together = ('visita', 'grado', 'seccion')

    def __str__(self):
        pass


class EjerciciosGrado(models.Model):
    """Registro de cantidad de estudiantes que realizan cierta cantidad de
    ejercicios en un :model:`kalite.Grado`.
    """

    grado = models.ForeignKey(Grado, related_name='ejercicios')
    estudiantes = models.PositiveIntegerField()
    ejercicios = models.PositiveIntegerField()

    class Meta:
        verbose_name = "EjerciciosGrado"
        verbose_name_plural = "EjerciciosGrados"
        unique_together = ('grado', 'ejercicios')

    def __str__(self):
        return '{} - {}'.format(self.estudiantes, self.ejercicios)
