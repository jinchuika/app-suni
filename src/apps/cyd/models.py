from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from easy_thumbnails.fields import ThumbnailerImageField

from apps.main.models import Municipio, Coordenada
from apps.escuela.models import Escuela


class Curso(models.Model):
    """
    Description: Curso de capacitación
    """
    nombre = models.CharField(max_length=75)
    nota_aprobacion = models.IntegerField()
    porcentaje = models.IntegerField()

    def get_total_asistencia(self):
        return sum(x.punteo_max for x in self.asistencia.all())

    def get_total_hito(self):
        return sum(x.punteo_max for x in self.hito.all())

    def get_absolute_url(self):
        return reverse('curso_detail', kwargs={"pk": self.id})

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


class Sede(models.Model):
    nombre = models.CharField(max_length=150)
    capacitador = models.ForeignKey(User)
    municipio = models.ForeignKey(Municipio)
    direccion = models.CharField(max_length=150)
    observacion = models.TextField(null=True, blank=True)
    mapa = models.ForeignKey(Coordenada, null=True, blank=True)

    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('sede_detail', kwargs={'pk': self.id})


class Grupo(models.Model):
    sede = models.ForeignKey(Sede)
    numero = models.IntegerField()
    curso = models.ForeignKey(Curso)
    comentario = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Grupo de capacitación"
        verbose_name_plural = "Grupos de capacitación"

    def __str__(self):
        return str(self.numero) + " - " + str(self.curso)


class Calendario(models.Model):
    cr_asistencia = models.ForeignKey(CrAsistencia)
    grupo = models.ForeignKey(Grupo)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    observacion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Calendario de grupos"
        verbose_name_plural = "Calendarios de grupos"


class ParRol(models.Model):
    nombre = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Rol de participante"
        verbose_name_plural = "Roles de participante"

    def __str__(self):
        return self.nombre


class ParEtnia(models.Model):
    nombre = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Etnia de participante"
        verbose_name_plural = "Etnias de participante"

    def __str__(self):
        return self.nombre


class ParEscolaridad(models.Model):
    nombre = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Escolaridad de participante"
        verbose_name_plural = "Escolaridades de participante"

    def __str__(self):
        return self.nombre


class Participante(models.Model):
    GENDER_CHOICES = (
        (1, 'Hombre'),
        (2, 'Mujer'),
    )

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    genero = models.IntegerField(choices=GENDER_CHOICES)
    rol = models.ForeignKey(ParRol, on_delete=models.PROTECT)
    escuela = models.ForeignKey(Escuela, on_delete=models.PROTECT)
    direccion = models.TextField(null=True, blank=True)
    mail = models.EmailField(null=True, blank=True)
    tel_casa = models.CharField(max_length=11, null=True, blank=True)
    tel_movil = models.CharField(max_length=11, null=True, blank=True)
    fecha_nac = models.DateField(null=True, blank=True)
    avatar = ThumbnailerImageField(
        upload_to="avatar_participante",
        null=True,
        blank=True,
        editable=True,)
    etnia = models.ForeignKey(ParEtnia, null=True, blank=True)
    escolaridad = models.ForeignKey(ParEscolaridad, null=True, blank=True)

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"

    def __str__(self):
        return self.nombre + " " + self.apellido

    def get_absolute_url(self):
        return ('')


class Asignacion(models.Model):
    participante = models.ForeignKey(Participante)
    grupo = models.ForeignKey(Grupo)

    class Meta:
        verbose_name = "Asignacion"
        verbose_name_plural = "Asignaciones"

    def __str__(self):
        return str(self.grupo) + " - " + str(self.participante)

    def get_absolute_url(self):
        return ('')
