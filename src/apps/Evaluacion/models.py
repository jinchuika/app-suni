from django.db import models
from apps.escuela import models as escuela_m
from apps.users import models as usuarios_m
from apps.cyd import models as cyd_m
from apps.escuela import models as esc_m
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class TipoRespuesta(models.Model):
    """Crea los tipos de respuesta posibles: texto/numero"""
    tipo_respuesta = models.CharField(max_length=10,verbose_name='Tipo_de_respuesta')

    class Meta:
        verbose_name = "Tipo de respuesta"
        verbose_name_plural = "Tipos de respuestas"

    def __str__(self):
        return self.tipo_respuesta
    

class AreaEvaluada(models.Model):
    """Crea las areas que puden ser evaluadas"""
    area_evaluada = models.CharField(max_length=30,verbose_name='area_evaluada')

    class Meta:
        verbose_name = "Area Evaluada"
        verbose_name_plural = "Areas Evaluadas"

    def __str__(self):
        return self.area_evaluada
    


class SeccionPregunta(models.Model):
    """La sección a la que pertenece un grupo de preguntas"""
    seccion_pregunta = models.CharField(max_length=40, verbose_name="seccion_pregunta")
    area_evaluada = models.ForeignKey(AreaEvaluada, on_delete=models.CASCADE, null=True, blank=True)
    activo = models.BooleanField(default=True)
    instrucciones = models.TextField(verbose_name='respuesta')


    class Meta: 
        verbose_name = "Sección Pregunta"
        verbose_name_plural = "Secciones de Preguntas"

    def __str__(self):
        return '{seccion} -> {area}'.format( seccion=self.seccion_pregunta, area =self.area_evaluada) 
    
class Evaluacion(models.Model):
    """Se crean el tipo de evaluación para asignarla a una area"""
    PONDERADA = "ponderada"
    NOPONDERADA = "no ponderada"

    TIPO_EVALUACION = (
        (PONDERADA, "Ponderada"),
        (NOPONDERADA, "No Ponderada"),
    )

    evaluacion = models.CharField(max_length=40, verbose_name="evaluacion")
    tipo_evaluacion = models.CharField(max_length=40, verbose_name='Tipo de evaluacion' , choices=TIPO_EVALUACION, default=NOPONDERADA)

    class Meta: 
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"

    def __str__(self):
        return self.evaluacion


class Pregunta(models.Model):
    """Expresa la pregunta, va asociado a una respuesta que a su vez esta asociado a un tipo de respuesta"""
    pregunta = models.CharField(max_length=200, verbose_name="Pregunta")    
    tipo_respuesta = models.ForeignKey(TipoRespuesta, related_name= "tipo_de_pregunta", null=True, blank=True,on_delete=models.CASCADE)
    area_evaluada = models.ForeignKey(AreaEvaluada, on_delete=models.CASCADE, null=True, blank=True)
    seccion_pregunta = models.ForeignKey(SeccionPregunta, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.BooleanField(default=True) 
    ponderacion = models.IntegerField(null=True, blank=True)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE,  null=True, blank=True)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"

    def __str__(self):
        return self.pregunta


class Respuesta(models.Model):
    """Contiene la respuesta, esta asociado al tipo de respuestas"""
    tipo_respuesta = models.ForeignKey(TipoRespuesta, on_delete=models.CASCADE) 
    respuesta = models.TextField(verbose_name='respuesta')

    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"

    def __str__(self):
        return self.respuesta


class Formulario(models.Model):
    """Contiene la información del formular"""
    activo = models.BooleanField(default= False) #Cambiar 
    escuela = models.ForeignKey(esc_m.Escuela, related_name='formulario_escuela', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='usuario', on_delete=models.CASCADE)
    fecha_inicio_formulario = models.DateTimeField( default=timezone.now, verbose_name='Fecha incio formulario')
    fecha_fin_formulario = models.DateTimeField(default=timezone.now, verbose_name='Fecha fin formulario')
    fecha_creacion_formulario = models.DateTimeField( default=timezone.now, verbose_name='Fecha creacion formulario')
    area_evaluada = models.ForeignKey(AreaEvaluada, on_delete=models.CASCADE, null=True, blank=True)
    formulario_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE,  null=True, blank=True)

    class Meta:
        verbose_name = "Formulario"
        verbose_name_plural = "Formularios"

    def __str__(self):
        return 'Escuela: {escuela} -> Capacitador: {capacitador}'.format(escuela =self.escuela, capacitador =self.usuario)


class AsignacionPregunta(models.Model):
    """Donde contiene información de la pregunta """
    respondido = models.BooleanField(default= False)
    formulario = models.ForeignKey(Formulario,  blank=True, null=True, on_delete=models.CASCADE)
    evaluado = models.ForeignKey(cyd_m.Participante, related_name='evaluado')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE,  blank=True, null=True,)
    respuesta = models.ForeignKey(Respuesta, blank=True, null=True, on_delete=models.CASCADE)
    fecha_incio_evaluacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha incio evaluacion')
    fecha_fin_evaluacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha fin evaluacion')
    
    class Meta:
        verbose_name = "Asignacion de pregunta"
        verbose_name_plural = "Asignacion de preguntas"

    def __str__(self):
        return '{formulario} - {pregunta}'.format(formulario=self.formulario.escuela, pregunta = self.pregunta)


class DispositivoParticipantes(models.Model):
    """Información del dispositivo desde donde se llena el formulario"""
    dispositivo = models.CharField(max_length=50,blank=True, null= True, verbose_name='Tipo_dispositivo')
    os = models.CharField(max_length=50,blank=True, null= True, verbose_name='Tipo_sistema_operativo')
    participante_info = models.ForeignKey(cyd_m.Participante, related_name='evaluado_dispositivo',  blank=True, null=True, )

    class Meta:
        verbose_name = "Informacion de dispositivo"
        verbose_name_plural = "Informacion de dispositivos"

    def __str__(self):
        return self.dispositivo
