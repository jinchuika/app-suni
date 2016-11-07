from operator import itemgetter
from django.db import models
from django.urls import reverse
from apps.main.models import Municipio
from apps.main.utils import get_telefonica
from apps.mye.models import Cooperante, Proyecto, Solicitud


class EscArea(models.Model):
    area = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'

    def __str__(self):
        return self.area


class EscJornada(models.Model):
    """
    Description: Jornada de la escuela
    """
    jornada = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Jornada'
        verbose_name_plural = 'Jornadas'

    def __str__(self):
        return self.jornada


class EscModalidad(models.Model):
    """
    Description: Modalidad de la escuela
    """
    modalidad = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Modalidad'
        verbose_name_plural = 'Modalidades'

    def __str__(self):
        return self.modalidad


class EscNivel(models.Model):
    """
    Description: Nivel de la escuela
    """
    nivel = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Nivel'
        verbose_name_plural = 'Niveles'

    def __str__(self):
        return self.nivel


class EscPlan(models.Model):
    """
    Description: Plan de la escuela (diario, fin de semana, etc.)
    """
    plan = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

    def __str__(self):
        return self.plan


class EscSector(models.Model):
    """
    Description: Sector de la escuela (oficial, privado, etc.)
    """
    sector = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'

    def __str__(self):
        return self.sector


class EscStatus(models.Model):
    """
    Description: Status de la escuela (Abierta, cerrada)
    """
    status = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statues'

    def __str__(self):
        return self.status


class Escuela(models.Model):
    """
    Description: Escuela
    """
    codigo = models.CharField(max_length=15, unique=True)
    distrito = models.CharField(max_length=10, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=250)
    direccion = models.TextField()
    telefono = models.CharField(max_length=12, null=True, blank=True)
    nivel = models.ForeignKey(EscNivel, on_delete=models.PROTECT)
    sector = models.ForeignKey(EscSector, on_delete=models.PROTECT)
    area = models.ForeignKey(EscArea, on_delete=models.PROTECT)
    status = models.ForeignKey(EscStatus, on_delete=models.PROTECT)
    modalidad = models.ForeignKey(EscModalidad, on_delete=models.PROTECT)
    jornada = models.ForeignKey(EscJornada, on_delete=models.PROTECT)
    plan = models.ForeignKey(EscPlan, on_delete=models.PROTECT)

    cooperante_asignado = models.ManyToManyField(
        Cooperante,
        through='mye.EscuelaCooperante',
        blank=True)
    proyecto_asignado = models.ManyToManyField(
        Proyecto,
        through='mye.EscuelaProyecto',
        blank=True)

    class Meta:
        verbose_name = "Escuela"
        verbose_name_plural = "Escuelas"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.id})

    def get_poblacion(self):
        poblacion_list = []
        for solicitud in Solicitud.objects.filter(escuela=self):
            poblacion_list.append({
                'fecha': solicitud.fecha,
                'alumnos': solicitud.total_alumno,
                'maestros': solicitud.total_maestro})
        return sorted(poblacion_list, key=itemgetter('fecha'))
    poblacion = property(get_poblacion)

    def get_poblacion_actual(self):
        poblacion_list = self.get_poblacion()
        if len(poblacion_list) > 0:
            return poblacion_list[0]['alumnos']
        else:
            return None
    poblacion_actual = property(get_poblacion_actual)

    def tiene_solicitud(self):
        return Solicitud.objects.filter(escuela=self).count() > 0


class EscContactoRol(models.Model):
    """
    Description: Rol para el contacto de escuela
    """
    rol = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Rol de contacto"
        verbose_name_plural = "Roles de contacto"

    def __str__(self):
        return self.rol


class EscContacto(models.Model):
    escuela = models.ForeignKey(Escuela, related_name="contacto")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rol = models.ForeignKey(EscContactoRol, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos de escuela"

    def __str__(self):
        return self.nombre + " " + self.apellido


class EscContactoTelefono(models.Model):
    contacto = models.ForeignKey(EscContacto, related_name="telefono", null=True)
    telefono = models.IntegerField()

    def get_empresa(self):
        return get_telefonica(self.telefono)
    empresa = property(get_empresa)

    def __str__(self):
        return str(self.telefono)


class EscContactoMail(models.Model):
    """
    Description: Correo de contacto
    """
    contacto = models.ForeignKey(EscContacto, related_name="mail", null=True)
    mail = models.EmailField(max_length=125)

    def __str__(self):
        return self.mail
