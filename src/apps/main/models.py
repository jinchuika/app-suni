import os
import json

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from django.test import Client
from django.core.files import File


class Departamento(models.Model):
    """
    Description: Departamento de Guatemala
    """
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    """
    Description: Municipio de Guatemala
    """
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre + " (" + str(self.departamento) + ")"


class Coordenada(models.Model):
    lat = models.CharField(max_length=25, verbose_name="Latitud")
    lng = models.CharField(max_length=25, verbose_name="Longitud")
    descripcion = models.CharField(max_length=70, null=True, blank=True, verbose_name="Descripción")

    def __str__(self):
        if self.descripcion:
            return self.descripcion
        else:
            return self.lat + ", " + self.lng


class ArchivoGenerado(models.Model):
    nombre = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    ultima_actualizacion = models.DateTimeField(default=timezone.now)
    archivo = models.FileField(upload_to='generados/')
    descripcion = models.TextField(null=True, blank=True)

    input_url = models.CharField(max_length=50, null=True, blank=True)
    activo = models.BooleanField(default=True, blank=True)

    class Meta:
        verbose_name = "Archivo fijo"
        verbose_name_plural = "Archivos fijos"

    def __str__(self):
        return self.nombre

    def generar_slug(self):
        fecha = timezone.now()
        return slugify('{}_{}'.format(self.nombre, fecha.strftime('%Y-%m-%d-%H-%M-%S')))

    def get_absolute_url(self):
        return settings.MEDIA_URL + self.archivo.name

    def generar(self):
        c = Client()
        res = c.get(reverse(self.input_url))
        slug = self.generar_slug()
        with open(settings.MEDIA_ROOT + '{}.json'.format(slug), "w") as f:
            json.dump(res.json(), f, ensure_ascii=False)

        with open(settings.MEDIA_ROOT + '{}.json'.format(slug), "r") as file:
            self.archivo.save('{}.json'.format(slug), File(file))
        os.remove(f.name)
