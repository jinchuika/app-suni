from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Colaborador(models.Model):
     """ Seguimiento de los comentario historicos que se haran en cada oferta
     """
     usuario = models.CharField(verbose_name="Nombre",max_length=150, null=True, blank=True)
     dpi = models.CharField(max_length=20, null=True, blank=True)
     email = models.CharField(verbose_name="Correo Electronico",max_length=150)
     fecha = models.DateTimeField(unique=True)
     edad = models.IntegerField(verbose_name="edad", null=True, blank=True)
     pregunta1 = models.CharField(verbose_name="¿ Padeces de alguna enfermedad o condición que te coloque en riesgo?",max_length=150, null=True, blank=True)
     pregunta2 = models.CharField(verbose_name="Si tu respuesta anterior fue afirmativa por favor explica brevemente la enfermedad o condición que te coloca en riesgo.",max_length=150, null=True, blank=True)
     pregunta3 = models.CharField(verbose_name="¿Tienes familiares que vivan contigo en esta época?",max_length=150, null=True, blank=True)
     pregunta4 = models.CharField(verbose_name="¿ Has presentado fiebre, tos, dolor de garganta, síntomas gastrointestinales (diarrea y/o vómito)  o dificultad para respirar en la últimas 24 horas?",max_length=150, null=True, blank=True)
     pregunta5 = models.CharField(verbose_name="¿Ha cambiado tu situación de salud desde la última vez que respondiste este formulario (solo responder del segundo en adelante)? ",max_length=150, null=True, blank=True)
     pregunta6 = models.CharField(verbose_name="Si tu respuesta anterior fue afirmativa por favor explica a continuación:",max_length=150, null=True, blank=True)
     pregunta7 = models.CharField(verbose_name="¿Cómo calificas tu estado emocional en este momento?",max_length=150, null=True, blank=True)
     pregunta8 = models.CharField(verbose_name="Explica brevemente tu situación mental o emocional en base a tu respuesta a la pregunta anterior.",max_length=150, null=True, blank=True)
     pregunta9 = models.CharField(verbose_name="¿Has registrado un cambio en cuanto al número de personas que viven contigo?",max_length=150, null=True, blank=True)
     pregunta10 = models.CharField(verbose_name="¿Tienes algún familiar o personas en casa que en las últimas 24 horas haya presentado alguno de los síntomas anteriores?",max_length=150, null=True, blank=True)
     pregunta11 = models.CharField(verbose_name="Si tu respuesta anterior fue afirmativa por favor explica a continuación:",max_length=150, null=True, blank=True)
     pregunta12 = models.CharField(verbose_name="¿Tuviste contacto con algún caso confirmado o sospechoso de COVID-19?",max_length=150, null=True, blank=True)
     pregunta13 = models.CharField(verbose_name="Si tu respuesta es afirmativa, ¿qué medidas tomaste?",max_length=150, null=True, blank=True)
     pregunta14 = models.CharField(verbose_name="¿Tiene tu colonia, municipio o comunidad donde vives cordón sanitario?",max_length=150, null=True, blank=True)
     pregunta15 = models.CharField(verbose_name="¿ Tienes familiares o personas que vivan contigo en una casa que tenga labores de alta exposición de contacto? (repartidores de alimentos, medicina, o recepcionista?",max_length=150, null=True, blank=True)
     pregunta16 = models.CharField(verbose_name="¿ Estás laborando actualmente en las instalaciones de la fundación?",max_length=150, null=True, blank=True)
     pregunta17 = models.CharField(verbose_name="¿Qué medidas de seguridad se están tomando dentro de las instalaciones de la fundación?",max_length=150, null=True, blank=True)

     class Meta:
         verbose_name = "Histórico de Bienestar"
         verbose_name_plural = "Históricos de Bienestar"

     def __str__(self):
         return str(self.usuario) + str(self.fecha)
