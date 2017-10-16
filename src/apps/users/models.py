from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from easy_thumbnails.fields import ThumbnailerImageField


class Organizacion(models.Model):
    COLOR_CHOICES = (
        ('#0073b7', 'azul'),
        ('#39cccc', 'aqua'),
        ('green', 'verde'),
        ('#f3c612', 'amarillo'),
        ('#dd4b39', 'rojo'),
        ('#605ca8', 'morado'),
        ('#f012be', 'rosa'),
        ('#ff851b', 'gris'),
        ('#777777', 'naranja'))

    nombre = models.CharField(max_length=150)
    color = models.CharField(max_length=20, default='#0073b7', choices=COLOR_CHOICES)

    class Meta:
        verbose_name = "Organización"
        verbose_name_plural = "Organizaciones"

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    COLOR_CHOICES = (
        ('#0073b7', 'azul'),
        ('#39cccc', 'aqua'),
        ('green', 'verde'),
        ('#f3c612', 'amarillo'),
        ('#dd4b39', 'rojo'),
        ('#605ca8', 'morado'),
        ('#f012be', 'rosa'),
        ('#ff851b', 'gris'),
        ('#777777', 'naranja'))
    GENERO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dpi = models.CharField(max_length=20, unique=True, null=True)
    public = models.BooleanField(default=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='M')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    foto = ThumbnailerImageField(
        upload_to="perfil_usuario",
        null=True,
        blank=True,
        editable=True,)
    color = models.CharField(max_length=20, default='#0073b7', choices=COLOR_CHOICES)

    organizacion = models.ForeignKey(
        Organizacion,
        verbose_name='Organización',
        on_delete=models.PROTECT,
        null=True,
        blank=True)

    def get_nombre(self):
        return self.user.first_name
    nombre = property(get_nombre)

    def get_apellido(self):
        return self.user.last_name
    apellido = property(get_apellido)

    def get_absolute_url(self):
        return reverse('perfil_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        return self.user.get_full_name()
