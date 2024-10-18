from random import randint
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.db.models import Count, F
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from easy_thumbnails.fields import ThumbnailerImageField

from apps.main.models import Municipio, Coordenada
from apps.escuela.models import Escuela


class Curso(models.Model):
    """Curso para impartir en la  capacitación."""

    GRUPO_CERTIFICADOS = (
        (1, "Tecnología Básica Nivel Intermedio"),
        (2, "NAAT 22 Semanas"),
        (3, "NAAT 18 Semanas")
    )

    nombre = models.CharField(max_length=75)
    nota_aprobacion = models.IntegerField()
    porcentaje = models.IntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True, blank=True, verbose_name='Activo')
    #grupo_certificado = models.IntegerField(choices=GRUPO_CERTIFICADOS, default=1)
    #grupos_certificado = models.IntegerField(choices=GRUPO_CERTIFICADOS, default=1)
    cyd_curso_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('curso_detail', kwargs={"pk": self.id})

    def get_total_asistencia(self):
        """Obtiene el total de puntos asignados a las asistencias."""
        return sum(x.punteo_max for x in self.asistencias.all())

    def get_total_hito(self):
        """Obtiene el total de puntos asignados a los hitos."""
        return sum(x.punteo_max for x in self.hitos.all())


class CrAsistencia(models.Model):
    """Período de asistencia establecido por el :class:`cyd.Curso`."""
    curso = models.ForeignKey(Curso, related_name="asistencias", on_delete=models.CASCADE)
    modulo_num = models.IntegerField()
    punteo_max = models.IntegerField()
    cyd_cr_asistencia_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)


    class Meta:
        #unique_together = ('curso', 'modulo_num',)  # Un curso no puede tener dos veces el mismo módulo
        verbose_name = "Asistencia de curso"
        verbose_name_plural = "Asistencias de curso"

    def __str__(self):
        return str(self.modulo_num) + " de " + str(self.curso)


class CrHito(models.Model):
    """Hito de :class:`cyd.Curso` (tareas, ejercicios, etc.)."""
    curso = models.ForeignKey(Curso, related_name="hitos", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40)
    punteo_max = models.IntegerField()
    cyd_cr_hito_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
  


    class Meta:
        verbose_name = "Hito de curso"
        verbose_name_plural = "Hitos de curso"

    def __str__(self):
        return str(self.nombre) + " de " + str(self.curso)


class Sede(models.Model):
    TIPO_SEDES = (
        ("B", "ESCUELA BENEFICIADA"),
        ("NB", "ESCUELA NO BENEFICIADA")
    )

    nombre = models.CharField(max_length=150)
    capacitador = models.ForeignKey(User, related_name='sedes', on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=150, verbose_name='Dirección')
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    mapa = models.ForeignKey(Coordenada, null=True, blank=True, on_delete=models.CASCADE)
    activa = models.BooleanField(default=True, blank=True, verbose_name='Activa')
    escuela_beneficiada = models.ForeignKey(Escuela, on_delete=models.PROTECT, related_name='escuela_beneficiada', blank=True, null=True)
    tipo_sede = models.CharField(max_length=2, verbose_name='Tipo de Sede' , choices=TIPO_SEDES, default='B')
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    url = models.TextField(null=True, blank=True,verbose_name='Carpeta Fotos')
    url_archivos = models.TextField(null=True, blank=True,verbose_name='Carpeta Archivos')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    finalizada = models.BooleanField(default=False, blank=True, verbose_name='Finalizada')
    finalizado_por = models.ForeignKey(User, related_name='finalizado', on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    
    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('sede_detail', kwargs={'pk': self.id})  
        
    def get_grupos(self):
        grupos = Grupo.objects.filter(sede=self).count()        
        return grupos
    
    def get_cursos_grupos(self):
        cursos_grupos = Grupo.objects.filter(sede=self)       
        return cursos_grupos

    def get_es_naat(self):
        grupos = Grupo.objects.filter(curso__nombre__icontains="NAAT",sede=self).count()
        if grupos >=1:
            return True
        else:
            return False        


    def get_escuelas(self):
        participantes = Participante.objects.filter(asignaciones__grupo__sede__id=self.id)        
        return Escuela.objects.filter(
            participantes__in=participantes).annotate(cantidad_participantes=Count('participantes')).distinct()
    
    def get_escuelas_invitadas(self):
        participantes = Participante.objects.filter(asignaciones__grupo__sede__id=self.id,asignaciones__grupo__numero=2,asignaciones__grupo__curso__nombre__icontains="Tecnologia")
        escuelas = Escuela.objects.filter(participantes__in=participantes).annotate(cantidad_participantes=Count('participantes')).distinct()             
        return escuelas 
               
    def save(self, *args, **kwargs):
        if self.url_archivos:
            string_url = str(self.url_archivos)
            validar_url= string_url.split('#grid')
            if not '' in validar_url:
                nueva_url=string_url.split('id=')
                #self.url_archivos='https://drive.google.com/embeddedfolderview?id='+nueva_url[1]+'#grid'
                self.url_archivos=string_url
        if self.url:
            string_url = str(self.url)
            validar_url= string_url.split('#grid')
            if not '' in validar_url:
                nueva_url=string_url.split('id=')
                #self.url='https://drive.google.com/embeddedfolderview?id='+nueva_url[1]+'#grid'
                self.url = string_url
        super(Sede, self).save(*args, **kwargs)

    def get_participantes(self):
        contador_ciclo_participantes=0
        invitada = False
        resultado = {'listado': [], 'resumen': {'roles': {}, 'genero': {}, 'estado': {}}}
        resultados_sede_invitada = {'listado':[]}
        participantes = Participante.objects.filter(
            asignaciones__grupo__sede__id=self.id, activo=True).annotate(
            cursos_sede=Count('asignaciones')).exclude(asignaciones__grupo__curso__nombre__icontains='Tecnologia', asignaciones__grupo__numero=2)        
        for participante in participantes:
            asignaciones = participante.asignaciones.filter(grupo__sede=self) 
            resultado['listado'].append({
                'participante': participante,
                'nota': sum(a.get_nota_promediada()['nota'] for a in asignaciones),
                'grupo': asignaciones.first().grupo.numero,
                'year':asignaciones.first().grupo.sede.fecha_creacion.year,
                'curso':asignaciones.first().grupo.curso.nombre
                
                })
        participantes_invitados = Participante.objects.filter(
            asignaciones__grupo__sede__id=self.id, activo=True, asignaciones__grupo__curso__nombre__icontains='Tecnologia', asignaciones__grupo__numero=2).annotate(
            cursos_sede=Count('asignaciones'))
        for participante_invitado in participantes_invitados:
            asignaciones_invitadas = participante_invitado.asignaciones.filter(grupo__sede=self)            
            resultado['listado'].append({
                'participante': participante_invitado,
                'nota': sum(a.get_nota_final() for a in asignaciones_invitadas),
                'grupo': asignaciones_invitadas.first().grupo.numero,
                'year':asignaciones_invitadas.first().grupo.sede.fecha_creacion.year,
                'curso':asignaciones_invitadas.first().grupo.curso.nombre
                
                })
        
        resultado['resumen']['roles'] = participantes.annotate(
            nombre_rol=F('rol__nombre')).values('nombre_rol').annotate(cantidad=Count('id', distinct=True))
        resultado['resumen']['genero'] = participantes.annotate(
            nombre_genero=F('genero__genero')).values('nombre_genero').annotate(cantidad=Count('id', distinct=True))
        aprobado = 0
        reprobado = 0
        nivelar = 0
        for data_listado in resultado['listado']:
            if data_listado['year']>=2024:
                if "NAAT" in data_listado['curso']:
                    if data_listado['nota'] >=61:
                        aprobado= aprobado +1
                    else:
                        reprobado = reprobado +1
                else:
                    if data_listado['nota'] >=70:
                        aprobado= aprobado +1
                    else:
                        reprobado = reprobado +1
                    
            else:
                 if data_listado['nota'] >=75:
                     aprobado = aprobado +1
                 elif data_listado['nota']<70:
                     reprobado = reprobado +1
                 elif  70 <= data_listado['nota'] <75:
                     nivelar= nivelar +1  

                
        aprobados = sum(1 for nota in resultado['listado'] if nota['nota'] >= 75)
        nivelars = sum(1 for nota in resultado['listado'] if 70 <= nota['nota'] < 75) #70 <= nota['nota'] < 75)
        reprobados = sum(1 for nota in resultado['listado'] if nota['nota'] < 70)
        reprobados_invitada =  sum(1 for nota in resultados_sede_invitada['listado'] if nota['nota'] < 70)
        aprobados_invitada =  sum(1 for nota in resultados_sede_invitada['listado'] if nota['nota'] >= 70)       
        sum_monitoreo = aprobado + nivelar +reprobado        
        if sum_monitoreo !=0:
            if nivelar !=0:
                monitoreo=False
            else:
                monitoreo=True
                #self.fecha_finalizacion = datetime.now() 
        else:
            monitoreo = False
        resultado['resumen']['monitoreo'] = monitoreo    
        resultado['resumen']['estado']['aprobado'] = {
            'cantidad': aprobado,
            'porcentaje': (aprobado * 100 // len(resultado['listado'])) if len(resultado['listado']) > 0 else 0}
        resultado['resumen']['estado']['nivelar'] = {
            'cantidad': nivelar,
            'porcentaje': (nivelar * 100 // len(resultado['listado'])) if len(resultado['listado']) > 0 else 0}
        resultado['resumen']['estado']['reprobado'] = {
            'cantidad': reprobado,
            'porcentaje': (reprobado * 100 // len(resultado['listado'])) if len(resultado['listado']) > 0 else 0}
        resultado['resumen']['estado']['invitada_reprobado'] ={
            'cantidad': reprobados_invitada,
            'porcentaje':(reprobados_invitada * 100 // len(resultados_sede_invitada['listado'])) if len(resultados_sede_invitada['listado']) > 0 else 0 }
        resultado['resumen']['estado']['invitada_aprobado'] ={
            'cantidad': aprobados_invitada,
            'porcentaje':(aprobados_invitada * 100 // len(resultados_sede_invitada['listado'])) if len(resultados_sede_invitada['listado']) > 0 else 0 }        
        return resultado


class Asesoria(models.Model):
    """Período en el que el capacitador está en la sede
    sin dar un módulo o asistencia.
    """
    sede = models.ForeignKey(Sede, related_name='asesorias', on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    cyd_asesorias_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = 'Período de asesoría'
        verbose_name_plural = 'Períodos de asesoría'

    def __str__(self):
        return '{} {}'.format(self.fecha, self.sede)


class Grupo(models.Model):
    """Grupo de capacitación"""
    sede = models.ForeignKey(Sede, related_name='grupos', on_delete=models.CASCADE)
    numero = models.IntegerField(verbose_name='Número')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    comentario = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True, blank=True, verbose_name='Activo')
    cyd_grupo_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Grupo de capacitación"
        verbose_name_plural = "Grupos de capacitación"
        #unique_together = ("sede", "numero", "curso")

    def __str__(self):
        return '{} - {}'.format(self.numero, self.curso)

    def get_absolute_url(self):
        return reverse_lazy('grupo_detail', kwargs={'pk': self.id})

    def get_hombres(self):
        return self.asignados.filter(participante__genero__id=1).count()

    def get_mujeres(self):
        return self.asignados.filter(participante__genero__id=2).count()

    def count_aprobados(self):
        cuenta = sum(1 for asignacion in self.asignados.all() if asignacion.aprobado)        
        return cuenta
    
    def count_reprobados(self):
        cuenta = sum(1 for asignacion in self.asignados.all() if asignacion.reprobado)        
        return cuenta         

    def get_porcentaje_aprobados(self):
        asignados = self.asignados.all().count()
        return self.count_aprobados() / asignados * 100 if asignados > 0 else 0

    def get_progreso_asistencias(self):
        """Cuenta la cantidad de de asistencias que ya se han impartido para este grupo.
        Indica también qué porcentaje del total representan,
        """
        asistencias_pasadas = self.asistencias.filter(fecha__lt=datetime.now()).count()
        try:
              porcentaje_actual = asistencias_pasadas / self.asistencias.all().count() * 100
        except ZeroDivisionError:
            porcentaje_actual=0

        return {'cantidad': asistencias_pasadas, 'porcentaje': porcentaje_actual}


class Calendario(models.Model):
    cr_asistencia = models.ForeignKey(CrAsistencia, verbose_name='Asistencia del curso', on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, related_name='asistencias', on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True, verbose_name='Hora de inicio')
    hora_fin = models.TimeField(null=True, blank=True, verbose_name='Hora de fin')
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    cyd_calendario_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

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
        return reverse_lazy('calendario_api_detail', kwargs={'pk': self.id})

    def count_asistentes(self):
        """Cuenta cuantos participantes asistieron."""
        return self.notas_asociadas.filter(nota__gt=0).count()  # type: int


class ParRol(models.Model):
    """Rol del participante."""
    nombre = models.CharField(max_length=50)
    #observaciones = models.CharField(max_length=100)
    cyd_rol_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Rol de participante"
        verbose_name_plural = "Roles de participante"

    def __str__(self):
        return self.nombre


class ParEtnia(models.Model):
    """Etnia del participante."""
    nombre = models.CharField(max_length=20)
    cyd_etnia_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Etnia de participante"
        verbose_name_plural = "Etnias de participante"

    def __str__(self):
        return self.nombre


class ParEscolaridad(models.Model):
    nombre = models.CharField(max_length=20)
    cyd_escolaridad_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = "Escolaridad de participante"
        verbose_name_plural = "Escolaridades de participante"

    def __str__(self):
        return self.nombre


class ParGenero(models.Model):
    """Género para el :class:`cyd.Participante`."""
    genero = models.CharField(max_length=8)
    cyd_genero_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

    def __str__(self):
        return self.genero
    
class Profesion(models.Model):
    nombre = models.CharField(max_length=20)


    class Meta:
        verbose_name = "Profesion"
        verbose_name_plural = "Profesiones"

    def __str__(self):
        return self.nombre
    
class Grado(models.Model):
    grado_asignado =  models.CharField(max_length=20)
    
    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"

    def __str__(self):
        return self.grado_asignado



class Participante(models.Model):
    """Participante de la capacitación por Funsepa."""
    dpi = models.CharField(max_length=15, unique=False, null=True, blank=True, db_index=True, error_messages={'Unico':"El dpi ya existe"})
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    genero = models.ForeignKey(ParGenero, null=True, on_delete=models.CASCADE)
    rol = models.ForeignKey(ParRol, on_delete=models.PROTECT)
    escuela = models.ForeignKey(Escuela, on_delete=models.PROTECT, related_name='participantes')
    direccion = models.TextField(null=True, blank=True, verbose_name='Dirección')
    mail = models.EmailField(null=True, blank=True)
    tel_casa = models.CharField(max_length=8, null=True, blank=True, verbose_name='Teléfono de casa')
    tel_movil = models.CharField(max_length=8, null=True, blank=True, verbose_name='Teléfono móvil')
    fecha_nac = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    avatar = ThumbnailerImageField(
        upload_to="avatar_participante",
        null=True,
        blank=True,
        editable=True,)
    etnia = models.ForeignKey(ParEtnia, null=True, blank=True, on_delete=models.CASCADE)
    escolaridad = models.ForeignKey(ParEscolaridad, null=True, blank=True, on_delete=models.CASCADE)    
    slug = models.SlugField(max_length=20, null=True, blank=True)
    activo = models.BooleanField(default=True, blank=True, verbose_name='Activo')
    profesion = models.ForeignKey(Profesion, null=True, blank=True, on_delete=models.CASCADE)
    grado_impartido = models.ForeignKey(Grado, null=True, blank=True, on_delete=models.CASCADE)
    chicos = models.IntegerField(default=0,verbose_name='niños')
    chicas = models.IntegerField(default=0,verbose_name='niñas')
    cyd_participante_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)

    def get_absolute_url(self):
        return reverse_lazy('participante_detail', kwargs={'pk': self.id})

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
        """Crea un registro de :class:`cyd.Asignacion` para el :class:`cyd.Participante`
        actual hacia un :class:`cyd.Grupo` especificado. Las notas son generadas
        automáticamente mediante `cyd.Asignacion.asignar_notas()`.
        """
        self.asignaciones.create(grupo=grupo)


class Asignacion(models.Model):
    """Asignación de un :class:`Participante` a un :class:`Grupo`."""
    participante = models.ForeignKey(Participante, related_name='asignaciones', on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, related_name='asignados', on_delete=models.CASCADE)
    abandono=models.BooleanField(default=False, blank=True, verbose_name='Abandono')
    #cyd_asignacion_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = "Asignación"
        verbose_name_plural = "Asignaciones"
        #unique_together = ('participante', 'grupo',)

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
        """Valida que un :class:`cyd.Participante` no pueda asignarse más
        de una vez al mismo :class:`cyd.Curso` en la misma :class:`cyd.Sede`.
        """
        super(Asignacion, self).validate_unique(*args, **kwargs)
        qs = Asignacion.objects.filter(grupo__sede=self.grupo.sede, grupo__curso=self.grupo.curso)
        if qs.filter(participante=self.participante).exists():
            self.abandono=True
            raise ValidationError({
                'grupo': ['No se puede asignar dos veces el mismo curso en la misma sede']})

    def get_absolute_url(self):
        """Se muestra en el perfil del :class:`cyd.Participante`."""
        return self.participante.get_absolute_url()

    def crear_notas(self):
        """Crea las notas especificadas en el :class:`cyd.Curso` del :class:`cyd.Grupo`
        relacionado con el objeto actual.
        """
        for calendario in self.grupo.asistencias.all():
            self.notas_asistencias.create(gr_calendario=calendario)
        for hito in self.grupo.curso.hitos.all():            
            self.notas_hitos.create(cr_hito=hito)

    def get_nota_final(self):       
        notas_asistencias = self.notas_asistencias.all()
        notas_hitos = self.notas_hitos.all()
        #print("Aca en el modelo:", sum(nota.nota for nota in notas_asistencias) + sum(nota.nota for nota in notas_hitos))
        return sum(nota.nota for nota in notas_asistencias) + sum(nota.nota for nota in notas_hitos)
    nota_final = property(get_nota_final)

    def get_aprobado(self):
        """Indica si la asignación actual alcanza la nota mínima establecida por el :class:`cyd.Curso`."""
        return self.get_nota_final() >= self.grupo.curso.nota_aprobacion  # type: boolean
    aprobado = property(get_aprobado)

    def get_reprobado(self):
        """Indica si la asignación actual alcanza la nota mínima establecida por el :class:`cyd.Curso`."""
        return self.get_nota_final() < self.grupo.curso.nota_aprobacion  # type: boolean
    reprobado = property(get_reprobado)

    def get_nota_promediada(self):
        """Devuelve la nota final promediada respecto al porcentaje del :class:`cyd.Curso` relacionado.
        En caso de que el curso no tenga un porcentaje, devuelve la nota final real.
        """    
        if self.grupo.curso.porcentaje:
            if(self.grupo.sede.get_grupos()==2):
                if(self.grupo.sede.get_cursos_grupos().filter(curso__id__in=[69,66]).exists()):
                    if(self.grupo.curso.id==69):
                        nota = self.get_nota_final() * (75 / 100)
                        promediada = True
                    else:
                        nota = self.get_nota_final() * (self.grupo.curso.porcentaje / 100)
                        promediada = True
                else:
                    nota = self.get_nota_final() * (self.grupo.curso.porcentaje / 100)
                    promediada = True
            else:
                nota = self.get_nota_final() * (self.grupo.curso.porcentaje / 100)
                promediada = True            
        else:            
            cantidad_asignaciones = Asignacion.objects.filter(
                grupo__sede=self.grupo.sede, participante=self.participante).count()           
            nota = self.get_nota_final() / cantidad_asignaciones
            promediada = False       
        return {'nota': nota, 'promediada': promediada}


class NotaAsistencia(models.Model):
    """Nota obtenida por el participante al llenar una asistencia."""
    asignacion = models.ForeignKey(Asignacion, related_name='notas_asistencias', on_delete=models.CASCADE)
    gr_calendario = models.ForeignKey(Calendario, related_name='notas_asociadas', on_delete=models.CASCADE)
    nota = models.IntegerField(default=0)
    #cyd_nota_asistencia_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
   

    class Meta:
        """No pueden existir dos registros de notas para el mismo período de capacitación."""
        verbose_name = "Nota de Asistencia"
        verbose_name_plural = "Notas de Asistencia"
        #unique_together = ('asignacion', 'gr_calendario',)

    def __str__(self):
        return '{} - {}'.format(self.nota, self.gr_calendario)

    def clean(self):
        """Evita que la nota sobrepase el punteo máximo especificado en :class:`CrAsistencia`

        Raises:
            ValidationError: La nota no puede exceder el punteo máximo.
        """
        if self.nota > self.gr_calendario.cr_asistencia.punteo_max:
            raise ValidationError({'nota': 'La nota no puede exceder el punteo máximo.'})


class NotaHito(models.Model):
    asignacion = models.ForeignKey(Asignacion, related_name='notas_hitos', on_delete=models.CASCADE)
    cr_hito = models.ForeignKey(CrHito, on_delete=models.CASCADE)
    nota = models.IntegerField(default=0)
    #cyd_nota_hito_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    

    class Meta:
        """No pueden existir dos registros de notas para el mismo hito."""
        verbose_name = "Nota de Hito"
        verbose_name_plural = "Notas de Hito"
        #unique_together = ('asignacion', 'cr_hito',)

    def __str__(self):
        return '{} - {}'.format(self.nota, self.cr_hito)

    def clean(self):
        """Evita que la nota sobrepase el punteo máximo especificado en :class:`CrHito`

        Raises:
            ValidationError: La nota no puede exceder el punteo máximo.
        """
        if self.nota > self.cr_hito.punteo_max:
            raise ValidationError({'nota': 'La nota no puede exceder el punteo máximo.'})

class RecordatorioCalendario(models.Model):
    """ Recordatorios del calendario
    """
    capacitador = models.ForeignKey(User, related_name='recordatorios', on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')

    class Meta:
        verbose_name = "Recordatorio"
        verbose_name_plural = "Recordatorios"

    def __str__(self):
        return '{} - {}'.format(self.capacitador, self.fecha)
