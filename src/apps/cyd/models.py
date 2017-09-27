from random import randint
from datetime import datetime, timedelta
from django.db import models
from django.db.models import Count, F
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from easy_thumbnails.fields import ThumbnailerImageField

from apps.main.models import Municipio, Coordenada
from apps.escuela.models import Escuela


class Curso(models.Model):
    """Curso para impartir en la  capacitación."""
    nombre = models.CharField(max_length=75)
    nota_aprobacion = models.IntegerField()
    porcentaje = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('curso_detail', kwargs={"pk": self.id})

    def get_total_asistencia(self):
        """Obtiene el total de puntos asignados a las asistencias."""
        return sum(x.punteo_max for x in self.asistencias.all())

    def get_total_hito(self):
        """Obtiene el total de puntos asignados a los hitos."""
        return sum(x.punteo_max for x in self.hitos.all())


class CrAsistencia(models.Model):
    """Período de asistencia establecido por el :model:`cyd.Curso`."""
    curso = models.ForeignKey(Curso, related_name="asistencias")
    modulo_num = models.IntegerField()
    punteo_max = models.IntegerField()

    class Meta:
        unique_together = ('curso', 'modulo_num',)  # Un curso no puede tener dos veces el mismo módulo
        verbose_name = "Asistencia de curso"
        verbose_name_plural = "Asistencias de curso"

    def __str__(self):
        return str(self.modulo_num) + " de " + str(self.curso)


class CrHito(models.Model):
    """Hito de :model:`cyd.Curso` (tareas, ejercicios, etc.)."""
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

    def get_escuelas(self):
        participantes = Participante.objects.filter(asignaciones__grupo__sede__id=self.id)
        return Escuela.objects.filter(participantes__in=participantes).annotate(cantidad_participantes=Count('participantes')).distinct()

    def get_participantes(self):
        resultado = {'listado': [], 'resumen': {'roles': {}, 'genero': {}, 'estado': {}}}
        participantes = Participante.objects.filter(
            asignaciones__grupo__sede__id=self.id).annotate(
            cursos_sede=Count('asignaciones'))
        print(participantes.query)
        for participante in participantes:
            asignaciones = participante.asignaciones.filter(grupo__sede=self)
            resultado['listado'].append({
                'participante': participante,
                'nota': sum(a.get_nota_promediada()['nota'] for a in asignaciones),
                'grupo': asignaciones.first().grupo.numero})
        resultado['resumen']['roles'] = participantes.annotate(nombre_rol=F('rol__nombre')).values('nombre_rol').annotate(cantidad=Count('id', distinct=True))
        resultado['resumen']['genero'] = participantes.annotate(nombre_genero=F('genero__genero')).values('nombre_genero').annotate(cantidad=Count('id', distinct=True))
        aprobado = sum(1 for nota in resultado['listado'] if nota['nota'] >= 75)
        nivelar = sum(1 for nota in resultado['listado'] if 70 <= nota['nota'] < 75)
        reprobado = sum(1 for nota in resultado['listado'] if nota['nota'] < 70)
        resultado['resumen']['estado']['aprobado'] = {
            'cantidad': aprobado,
            'porcentaje': (aprobado * 100 // len(resultado['listado'])) if len(resultado['listado']) > 0 else 0}
        resultado['resumen']['estado']['nivelar'] = {
            'cantidad': nivelar,
            'porcentaje': (nivelar * 100 // len(resultado['listado'])) if len(resultado['listado']) > 0 else 0}
        resultado['resumen']['estado']['reprobado'] = {
            'cantidad': reprobado,
            'porcentaje': (reprobado * 100 // len(resultado['listado'])) if len(resultado['listado']) > 0 else 0}
        return resultado


class Asesoria(models.Model):
    """Período en el que el capacitador está en la sede
    sin dar un módulo o asistencia.
    """
    sede = models.ForeignKey(Sede, related_name='asesorias')
    fecha = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')

    class Meta:
        verbose_name = 'Período de asesoría'
        verbose_name_plural = 'Períodos de asesoría'

    def __str__(self):
        return '{} {}'.format(self.fecha, self.sede)


class Grupo(models.Model):
    """Grupo de capacitación"""
    sede = models.ForeignKey(Sede, related_name='grupos')
    numero = models.IntegerField(verbose_name='Número')
    curso = models.ForeignKey(Curso)
    comentario = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Grupo de capacitación"
        verbose_name_plural = "Grupos de capacitación"
        unique_together = ("sede", "numero", "curso")

    def __str__(self):
        return '{} - {}'.format(self.numero, self.curso)

    def get_absolute_url(self):
        return reverse('grupo_detail', kwargs={'pk': self.id})

    def get_hombres(self):
        return self.asignados.filter(participante__genero__id=1).count()

    def get_mujeres(self):
        return self.asignados.filter(participante__genero__id=2).count()

    def count_aprobados(self):
        cuenta = sum(1 for asignacion in self.asignados.all() if asignacion.aprobado)
        return cuenta

    def get_porcentaje_aprobados(self):
        asignados = self.asignados.all().count()
        return self.count_aprobados() / asignados * 100 if asignados > 0 else 0

    def get_progreso_asistencias(self):
        """Cuenta la cantidad de de asistencias que ya se han impartido para este grupo.
        Indica también qué porcentaje del total representan,
        """
        asistencias_pasadas = self.asistencias.filter(fecha__lt=datetime.now()).count()
        porcentaje_actual = asistencias_pasadas / self.asistencias.all().count() * 100
        return {'cantidad': asistencias_pasadas, 'porcentaje': porcentaje_actual}


class Calendario(models.Model):
    cr_asistencia = models.ForeignKey(CrAsistencia, verbose_name='Asistencia del curso')
    grupo = models.ForeignKey(Grupo, related_name='asistencias')
    fecha = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True, verbose_name='Hora de inicio')
    hora_fin = models.TimeField(null=True, blank=True, verbose_name='Hora de fin')
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')

    class Meta:
        verbose_name = "Calendario de grupos"
        verbose_name_plural = "Calendarios de grupos"

    def __str__(self):
        return str(self.cr_asistencia.modulo_num) + " - Grupo " + str(self.grupo)

    def save(self, *args, **kwargs):
        # si el objeto no tiene hora de fin, asigna 90 minutos extras
        if self.hora_inicio and not self.hora_fin:
            fecha = self.fecha if self.fecha else datetime(2000, 1, 1)
            self.hora_fin = (datetime.combine(fecha, self.hora_inicio) + timedelta(minutes=90)).time()
        super(Calendario, self).save(*args, **kwargs)

    def get_api_url(self):
        return reverse('calendario_api_detail', kwargs={'pk': self.id})

    def count_asistentes(self):
        """Cuenta cuantos participantes asistieron."""
        return self.notas_asociadas.filter(nota__gt=0).count()  # type: int


class ParRol(models.Model):
    """Rol del participante."""
    nombre = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Rol de participante"
        verbose_name_plural = "Roles de participante"

    def __str__(self):
        return self.nombre


class ParEtnia(models.Model):
    """Etnia del participante."""
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


class ParGenero(models.Model):
    """Género para el :model:`cyd.Participante`."""
    genero = models.CharField(max_length=8)

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

    def __str__(self):
        return self.genero


class Participante(models.Model):
    """Participante de la capacitación por Funsepa."""
    dpi = models.CharField(max_length=21, unique=True, null=True, blank=True, db_index=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    genero = models.ForeignKey(ParGenero, null=True)
    rol = models.ForeignKey(ParRol, on_delete=models.PROTECT)
    escuela = models.ForeignKey(Escuela, on_delete=models.PROTECT, related_name='participantes')
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

    slug = models.SlugField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)

    def get_absolute_url(self):
        return reverse('participante_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """En caso de que el participante no tenga DPI, se le asigna uno temporal.
        El DPI creado sigue el patrón:
        f-{correlativo}-{random}
        El número aleatorio entre 100 y 999 asegura que dos participantes creados al mismo tiempo
        no tengan el mismo correlativo (para los casos en los que la base de datos no realiza el proceso
        de crear lo suficientemente rápido.)
        """
        if not self.dpi:
            temp_id = self.id if self.pk else (Participante.objects.values('id').last()['id'] + 1)
            self.dpi = "f-{}-{}".format(temp_id, randint(100, 999))
        # aseguramos de tener el dpi como slug para el participante
        self.slug = slugify(self.dpi)
        super(Participante, self).save(*args, **kwargs)

    def asignar(self, grupo):
        """Crea un registro de :model:`cyd.Asignacion` para el :model:`cyd.Participante` 
        actual hacia un :model:`cyd.Grupo` especificado. Las notas son generadas
        automáticamente mediante `cyd.Asignacion.asignar_notas()`.
        """
        self.asignaciones.create(grupo=grupo)


class Asignacion(models.Model):
    """Asignación de un participante a un grupo."""
    participante = models.ForeignKey(Participante, related_name='asignaciones')
    grupo = models.ForeignKey(Grupo, related_name='asignados')

    class Meta:
        verbose_name = "Asignación"
        verbose_name_plural = "Asignaciones"
        unique_together = ('participante', 'grupo',)

    def __str__(self):
        return '{} - {}'.format(self.grupo, self.participante)

    def save(self, *args, **kwargs):
        """Crea todos los registros de notas necesarias en caso de que el objeto actual no tenga `pk`."""
        if not self.pk:
            super(Asignacion, self).save(*args, **kwargs)
            self.crear_notas()
        else:
            super(Asignacion, self).save(*args, **kwargs)

    def validate_unique(self, *args, **kwargs):
        """Valida que un :model:`cyd.Participante` no pueda asignarse más
        de una vez al mismo :model:`cyd.Curso` en la misma :model:`cyd.Sede`.
        """
        super(Asignacion, self).validate_unique(*args, **kwargs)
        qs = Asignacion.objects.filter(grupo__sede=self.grupo.sede, grupo__curso=self.grupo.curso)
        if qs.filter(participante=self.participante).exists():
            raise ValidationError({
                'grupo': ['No se puede asignar dos veces el mismo curso en la misma sede']})

    def get_absolute_url(self):
        """Se muestra en el perfil del :model:`cyd.Participante`."""
        return self.participante.get_absolute_url()

    def crear_notas(self):
        """Crea las notas especificadas en el :model:`cyd.Curso` del :model:`cyd.Grupo`
        relacionado con el objeto actual.
        """
        for calendario in self.grupo.asistencias.all():
            self.notas_asistencias.create(gr_calendario=calendario)
        for hito in self.grupo.curso.hitos.all():
            self.notas_hitos.create(cr_hito=hito)

    def get_nota_final(self):
        return sum(nota.nota for nota in self.notas_asistencias.all()) + sum(nota.nota for nota in self.notas_hitos.all())
    nota_final = property(get_nota_final)

    def get_aprobado(self):
        """Indica si la asignación actual alcanza la nota mínima establecida por el :model:`cyd.Curso`."""
        return self.get_nota_final() >= self.grupo.curso.nota_aprobacion  # type: boolean
    aprobado = property(get_aprobado)

    def get_nota_promediada(self):
        """Devuelve la nota final promediada respecto al porcentaje del :model:`cyd.Curso` relacionado.
        En caso de que el curso no tenga un porcentaje, devuelve la nota final real.
        """
        if self.grupo.curso.porcentaje:
            nota = self.get_nota_final() * (self.grupo.curso.porcentaje / 100)
            promediada = True
        else:
            cantidad_asignaciones = Asignacion.objects.filter(grupo__sede=self.grupo.sede, participante=self.participante).count()
            nota = self.get_nota_final() / cantidad_asignaciones
            promediada = False
        return {'nota': nota, 'promediada': promediada}


class NotaAsistencia(models.Model):
    """Nota obtenida por el participante al llenar una asistencia."""
    asignacion = models.ForeignKey(Asignacion, related_name='notas_asistencias')
    gr_calendario = models.ForeignKey(Calendario, related_name='notas_asociadas')
    nota = models.IntegerField(default=0)

    class Meta:
        """No pueden existir dos registros de notas para el mismo período de capacitación."""
        verbose_name = "Nota de Asistencia"
        verbose_name_plural = "Notas de Asistencia"
        unique_together = ('asignacion', 'gr_calendario',)

    def __str__(self):
        return '{} - {}'.format(self.nota, self.gr_calendario)

    def clean(self):
        """Evita que la nota sobrepase el punteo máximo especificado en :model:`CrAsistencia`

        Raises:
            ValidationError: La nota no puede exceder el punteo máximo.
        """
        if self.nota > self.gr_calendario.cr_asistencia.punteo_max:
            raise ValidationError({'nota': 'La nota no puede exceder el punteo máximo.'})


class NotaHito(models.Model):
    asignacion = models.ForeignKey(Asignacion, related_name='notas_hitos')
    cr_hito = models.ForeignKey(CrHito)
    nota = models.IntegerField(default=0)

    class Meta:
        """No pueden existir dos registros de notas para el mismo hito."""
        verbose_name = "Nota de Hito"
        verbose_name_plural = "Notas de Hito"
        unique_together = ('asignacion', 'cr_hito',)

    def __str__(self):
        return '{} - {}'.format(self.nota, self.cr_hito)

    def clean(self):
        """Evita que la nota sobrepase el punteo máximo especificado en :model:`CrHito`

        Raises:
            ValidationError: La nota no puede exceder el punteo máximo.
        """
        if self.nota > self.cr_hito.punteo_max:
            raise ValidationError({'nota': 'La nota no puede exceder el punteo máximo.'})
