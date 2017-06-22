from datetime import datetime, timedelta
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
        return sum(x.punteo_max for x in self.asistencias.all())

    def get_total_hito(self):
        return sum(x.punteo_max for x in self.hitos.all())

    def get_absolute_url(self):
        return reverse('curso_detail', kwargs={"pk": self.id})

    def __str__(self):
        return self.nombre


class CrAsistencia(models.Model):
    """
    Description: Asistencia a curso
    """
    curso = models.ForeignKey(Curso, related_name="asistencias")
    modulo_num = models.IntegerField()
    punteo_max = models.IntegerField()

    class Meta:
        unique_together = ('curso', 'modulo_num',)
        verbose_name = "Asistencia de curso"
        verbose_name_plural = "Asistencias de curso"

    def __str__(self):
        return str(self.modulo_num) + " de " + str(self.curso)


class CrHito(models.Model):
    """
    Description: Hito a curso
    """
    curso = models.ForeignKey(Curso, related_name="hitos")
    nombre = models.CharField(max_length=40)
    punteo_max = models.IntegerField()

    class Meta:
        verbose_name = "Hito de curso"
        verbose_name_plural = "Hitos de curso"

    def __str__(self):
        return str(self.nombre) + " de " + str(self.curso)


class Sede(models.Model):
    nombre = models.CharField(max_length=150)
    capacitador = models.ForeignKey(User, related_name='sedes')
    municipio = models.ForeignKey(Municipio)
    direccion = models.CharField(max_length=150, verbose_name='Dirección')
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    mapa = models.ForeignKey(Coordenada, null=True, blank=True)

    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('sede_detail', kwargs={'pk': self.id})


class Grupo(models.Model):
    sede = models.ForeignKey(Sede, related_name='grupos')
    numero = models.IntegerField(verbose_name='Número')
    curso = models.ForeignKey(Curso)
    comentario = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Grupo de capacitación"
        verbose_name_plural = "Grupos de capacitación"
        unique_together = ("sede", "numero")

    def __str__(self):
        return str(self.numero) + " - " + str(self.curso)

    def get_absolute_url(self):
        return reverse('grupo_detail', kwargs={'pk': self.id})


class Calendario(models.Model):
    cr_asistencia = models.ForeignKey(CrAsistencia)
    grupo = models.ForeignKey(Grupo, related_name='asistencias')
    fecha = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Calendario de grupos"
        verbose_name_plural = "Calendarios de grupos"

    def __str__(self):
        return str(self.cr_asistencia.modulo_num) + " - Grupo " + str(self.grupo)

    def save(self, *args, **kwargs):
        if self.hora_inicio and not self.hora_fin:
            fecha = self.fecha if self.fecha else datetime(2000, 1, 1)
            self.hora_fin = (datetime.combine(fecha, self.hora_inicio) + timedelta(minutes=90)).time()
        super(Calendario, self).save(*args, **kwargs)

    def get_api_url(self):
        return reverse('calendario_api_detail', kwargs={'pk': self.id})


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
        ("M", 'Hombre'),
        ("F", 'Mujer'),
    )

    dpi = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    genero = models.CharField(choices=GENDER_CHOICES, max_length=1)
    rol = models.ForeignKey(ParRol, on_delete=models.PROTECT)
    escuela = models.ForeignKey(Escuela, on_delete=models.PROTECT)
    direccion = models.TextField(null=True, blank=True, verbose_name='Dirección')
    mail = models.EmailField(null=True, blank=True)
    tel_casa = models.CharField(max_length=11, null=True, blank=True, verbose_name='Teléfono de casa')
    tel_movil = models.CharField(max_length=11, null=True, blank=True, verbose_name='Teléfono móvil')
    fecha_nac = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
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
        return '{} {}'.format(self.nombre, self.apellido)

    def get_absolute_url(self):
        return ('')


class Asignacion(models.Model):
    participante = models.ForeignKey(Participante, related_name='asignaciones')
    grupo = models.ForeignKey(Grupo, related_name='asignados')

    class Meta:
        verbose_name = "Asignación"
        verbose_name_plural = "Asignaciones"

    def __str__(self):
        return '{} - {}'.format(self.grupo, self.participante)

    def get_absolute_url(self):
        return ('')
