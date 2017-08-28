from django.db import models
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from apps.escuela.models import Escuela


class Rubrica(models.Model):
    """Rúbrica para evaluar el rendimiento de la :model:`kalite.Visita`."""
    AQUA = 'aqua'
    GREEN = 'green'
    YELLOW = 'yellow'
    RED = 'red'
    PRUPLE = 'purple'
    COLOR_CHOICES = (
        (AQUA, 'aqua'),
        (GREEN, 'green'),
        (YELLOW, 'yellow'),
        (RED, 'red'),
        (PRUPLE, 'purple'))

    nombre = models.CharField(max_length=35)
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    color = models.CharField(max_length=20, default="aqua", choices=COLOR_CHOICES)
    icon = models.CharField(max_length=25, default="fa-check-square-o")

    class Meta:
        verbose_name = "Rúbrica"
        verbose_name_plural = "Rúbricas"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('rubrica_detail', kwargs={'pk': self.id})


class TipoVisita(models.Model):
    """Indica qué :model:`kalite.Rubrica`s aplican para la :model:`kalite.Visita`.
    En base al listado que tenga relacionado este objeto, se pueden crear
    las :model:`kalite.Evaluacion` correspondientes.
    """
    nombre = models.CharField(max_length=30)
    rubricas = models.ManyToManyField(Rubrica)

    class Meta:
        verbose_name = "Tipo de Visita"
        verbose_name_plural = "Tipos de Visita"

    def __str__(self):
        return self.nombre


class Visita(models.Model):
    """Visita de seguimiento de KA Lite después de que la escuela ha
    recibido la capacitación.
    """

    escuela = models.ForeignKey(Escuela, related_name='visitas_kalite')
    tipo_visita = models.ForeignKey(TipoVisita)
    fecha = models.DateField()
    hora_inicio = models.TimeField(null=True, blank=True, verbose_name='Hora de inicio')
    hora_fin = models.TimeField(null=True, blank=True, verbose_name='Hora de fin')
    capacitador = models.ForeignKey(User, related_name='visitas_kalite')
    numero = models.PositiveIntegerField(default=1)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Visita de KA Lite"
        verbose_name_plural = "Visitas de KA Lite"
        unique_together = ('escuela', 'numero')

    def __str__(self):
        return '{} - {}'.format(self.fecha, self.escuela)

    def get_absolute_url(self):
        return reverse_lazy('visita_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Al registrar este objeto en la base de datos, crea las
        :model:`kalite.Evaluacion`es indicadas en `tipo_visita`.
        """
        if not self.pk:
            super(Visita, self).save(*args, **kwargs)
            self.crear_evaluaciones()
        else:
            super(Visita, self).save(*args, **kwargs)

    def crear_evaluaciones(self):
        """Crea las :model:`kalite.Evaluacion`s indicadas por el
        :model:`kalite.TipoVisita` de este objeto.
        """
        for rubrica in self.tipo_visita.rubricas.all():
            self.evaluaciones.create(rubrica=rubrica)

    @property
    def promedio(self):
        evaluaciones_count = self.evaluaciones.count()
        if evaluaciones_count > 0:
            promedio = sum(e.promedio for e in self.evaluaciones.all()) / self.evaluaciones.count()
        else:
            promedio = 0
        return round(promedio, 2)

    @property
    def estado(self):
        promedio = self.promedio
        if promedio >= 75:
            return {'alcance': 'Alto', 'color': 'green'}
        elif promedio >= 55:
            return {'alcance': 'Mediano', 'color': 'yellow'}
        else:
            return {'alcance': 'Bajo', 'color': 'red'}


class Indicador(models.Model):
    """Indicador a evaluar de la :model:`kalite.Rubrica`."""
    rubrica = models.ForeignKey(Rubrica, related_name='indicadores')
    indicador = models.TextField()

    class Meta:
        verbose_name = "Indicador"
        verbose_name_plural = "Indicadores"

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
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        unique_together = ('visita', 'rubrica')

    def __str__(self):
        return '{} - {}'.format(self.rubrica, self.visita)

    def get_absolute_url(self):
        return self.visita.get_absolute_url()

    def save(self, *args, **kwargs):
        """Para crear los :model:`kalite.Punteo`s al registrar
        este objeto por primera vez en la base de datos.
        """
        if not self.pk:
            super(Evaluacion, self).save(*args, **kwargs)
            self.crear_notas()
        else:
            super(Evaluacion, self).save(*args, **kwargs)

    def crear_notas(self):
        """Crea los registros de :model:`kalite.Punteo` asociados a la
        :model:`kalite.Rubrica` de este objeto en particular.
        """
        for indicador in self.rubrica.indicadores.all():
            self.notas.create(indicador=indicador)

    @property
    def promedio(self):
        notas_count = self.notas.count()
        if notas_count > 0:
            promedio = sum(n.nota for n in self.notas.all()) / notas_count
        else:
            promedio = 0
        return round(20 * promedio, 2)


class Punteo(models.Model):
    """Punteo asignado a un :model:`kalite.Indicador` durante
    una :model:`kalite.Evaluacion`.

    Las opciones de `nota` son constantes "privadas" para la clase.
    `MULTIPLICADOR` es el factor para las opciones de `nota`.
    """
    NOTA_1 = 1
    NOTA_2 = 2
    NOTA_3 = 3
    NOTA_4 = 4
    NOTA_5 = 5
    MULTIPLICADOR = 20
    NOTA_CHOICES = (
        (NOTA_1, '{}%'.format(MULTIPLICADOR * NOTA_1)),
        (NOTA_2, '{}%'.format(MULTIPLICADOR * NOTA_2)),
        (NOTA_3, '{}%'.format(MULTIPLICADOR * NOTA_3)),
        (NOTA_4, '{}%'.format(MULTIPLICADOR * NOTA_4)),
        (NOTA_5, '{}%'.format(MULTIPLICADOR * NOTA_5)))

    evaluacion = models.ForeignKey(Evaluacion, related_name='notas')
    indicador = models.ForeignKey(Indicador)
    nota = models.IntegerField(choices=NOTA_CHOICES, default=NOTA_1)

    class Meta:
        verbose_name = "Punteo"
        verbose_name_plural = "Punteos"
        unique_together = ('evaluacion', 'indicador')

    def __str__(self):
        return '{indicador}... - {porcentaje}%'.format(
            indicador=str(self.indicador)[:15],
            porcentaje=self.nota * self.MULTIPLICADOR)

    @property
    def multiplicador(self):
        return self.MULTIPLICADOR

    @property
    def valor(self):
        return self.nota * self.multiplicador

    @classmethod
    def notas(self):
        return [self.NOTA_1, self.NOTA_2, self.NOTA_3, self.NOTA_4, self.NOTA_5]


class Grado(models.Model):
    """Registro de grado (con sección) durante una :model:`kalite.Visita`."""

    visita = models.ForeignKey(Visita, related_name='grados')
    grado = models.IntegerField()
    seccion = models.CharField(max_length=2, null=True, blank=True, verbose_name='Sección')
    minimo_esperado = models.PositiveIntegerField(verbose_name='Mínimo esperado', default=1)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
        unique_together = ('visita', 'grado', 'seccion')

    def __str__(self):
        return '{} {}'.format(self.grado, self.seccion)

    def get_api_url(self):
        return reverse_lazy('grado_api_detail', kwargs={'pk': self.pk})

    @property
    def total_estudiantes(self):
        return sum(e.estudiantes for e in self.ejercicios.all())

    @property
    def total_ejercicios(self):
        return sum(e.estudiantes * e.ejercicios for e in self.ejercicios.all())

    @property
    def alcanzados(self):
        """Cantidad de estudiantes que alcanzaron la cantidad mínima de ejercicios.
        """
        return sum(
            e.estudiantes for e in self.ejercicios.all()
            if e.ejercicios >= self.minimo_esperado)

    @property
    def nivelar(self):
        """Cantidad de estudiantes que NO alcanzaron la cantidad mínima de ejercicios.
        """
        return self.total_estudiantes - self.alcanzados

    @property
    def promedio_ejercicios(self):
        """Calcula la cantidad de ejercicios realizados, en promedio, por
        un estudiante.
        """
        if self.total_ejercicios == 0:
            return 0
        else:
            return round(self.total_ejercicios / self.total_estudiantes, 2)

    @property
    def promedio_alcanzados(self):
        if self.alcanzados == 0:
            return 0
        else:
            return round(self.alcanzados / self.total_estudiantes, 2)


class EjerciciosGrado(models.Model):
    """Registro de cantidad de estudiantes que realizan cierta cantidad de
    ejercicios en un :model:`kalite.Grado`.
    """

    grado = models.ForeignKey(Grado, related_name='ejercicios')
    estudiantes = models.PositiveIntegerField(default=0)
    ejercicios = models.PositiveIntegerField()

    class Meta:
        verbose_name = "EjerciciosGrado"
        verbose_name_plural = "EjerciciosGrados"
        unique_together = ('grado', 'ejercicios')

    def __str__(self):
        return '{} - {}'.format(self.estudiantes, self.ejercicios)

    def get_api_url(self):
        return reverse_lazy('ejerciciosgrado_api_detail', kwargs={'pk': self.pk})
