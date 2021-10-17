from django.db import models
from django.urls import reverse_lazy
from apps.escuela.models import Escuela
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Materia(models.Model):
    """ Modelo para guardar  el nombre de las materias , asignarles un color y
    colocarles un icono
    """
    COLOR_CHOICES = (
        ('navy', 'azul'),
        ('aqua', 'aqua'),
        ('purple', 'Morado'),
        ('yellow', 'Amarillo'),
        ('teal', 'turquesa'),
        ('red', 'rojo'),
        ('green', 'verde'),)

    nombre = models.CharField(max_length=35)
    color = models.CharField(default='green', choices=COLOR_CHOICES, max_length=20)
    icon = models.CharField(max_length=25,default='fa-check-square-o')
    materia_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre

class Grado(models.Model):
    """Se guardan el nombre de los grados"""
    nombre_grado = models.CharField(max_length=35,verbose_name="nombre")
    cn_grado_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,related_name="cn_grado_creado_por",default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'

    def __str__(self):
        return self.nombre_grado

class Semestre(models.Model):
    """Guarada el semestre correspondiente"""
    numero = models.IntegerField()
    cn_semestre_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = 'Semestre'
        verbose_name_plural = 'Semestres'

    def __str__(self):
        return str(self.numero)

class Visita(models.Model):
    """Guarda la informacion correspondiente a las visitas hechas por el capacitador"""
    escuela= models.ForeignKey(Escuela, related_name='escuelas', on_delete=models.CASCADE)
    semestre= models.ForeignKey(Semestre, related_name='semestres', on_delete=models.CASCADE)
    usuario= models.ForeignKey(User, related_name='usuarios', on_delete=models.CASCADE)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    numero_visita= models.IntegerField()
    fecha = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'

    def __str__(self):
        return '{} {} {} {}'.format(self.usuario,self.semestre,self.fecha, self.escuela)

class Evaluacion(models.Model):
    """Modelo para guardar los datos de las evaluacion, de los grados hechas por  el capacitador"""
    visita = models.ForeignKey(Visita, related_name='visitas', on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, related_name='materias', on_delete=models.CASCADE)
    grado = models.ForeignKey(Grado, related_name='grados', on_delete=models.CASCADE)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    cn_evaluacion_creado_por =models.ForeignKey(User, on_delete=models.CASCADE, related_name="cn_evaluacion_creado_por",default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = 'Evaluacion'
        verbose_name_plural = 'Evaluaciones'
        ordering = ('visita',)

    def __str__(self):
        return str(self.visita)

class Notas(models.Model):
    """ guarda las notas obteniadas por el alumno."""
    evaluacion= models.ForeignKey(Evaluacion, related_name='notas', on_delete=models.CASCADE)
    alumno=models.CharField(max_length=250,verbose_name="nombre del alumno")
    nota= models.IntegerField()
    cn_notas_creado_por =models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return '{} {}'.format(self.alumno, self.nota)
