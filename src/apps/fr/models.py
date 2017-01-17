from django.db import models
from django.urls import reverse_lazy


class Empresa(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=12, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('empresa_detail', kwargs={'empresa_pk': self.id})


class TipoEvento(models.Model):
    tipo_evento = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Tipo de evento'
        verbose_name_plural = 'Tipos de eventos'

    def __str__(self):
        return self.tipo_evento


class Evento(models.Model):
    COLOR_CHOICES = (
        ('navy', 'azul'),
        ('aqua', 'aqua'),
        ('purple', 'Morado'),
        ('yellow', 'Amarillo'),
        ('teal', 'turquesa'),
        ('red', 'rojo'),
        ('green', 'verde'),)

    nombre = models.CharField(max_length=50)
    tipo_de_evento = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    color = models.CharField(default='green', choices=COLOR_CHOICES, max_length=10)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    COLOR_CHOICES = (
        ('navy', 'azul'),
        ('aqua', 'aqua'),
        ('purple', 'Morado'),
        ('yellow', 'Amarillo'),
        ('teal', 'turquesa'),
        ('red', 'rojo'),
        ('green', 'verde'),)

    etiqueta = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    color = models.CharField(default='purple', choices=COLOR_CHOICES, max_length=10)

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ('etiqueta',)

    def __str__(self):
        return self.etiqueta


class Contacto(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='contacto')
    nombre = models.CharField(max_length=70)
    apellido = models.CharField(max_length=70)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    etiquetas = models.ManyToManyField(Etiqueta, related_name='contacto')
    evento = models.ManyToManyField(Evento, related_name='contacto')
    observacion = models.TextField(null=True, blank=True)
    puesto = models.CharField(max_length=75)

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

    def __str__(self):
        return self.nombre + " " + self.apellido


class ContactoMail(models.Model):
    mail = models.EmailField(max_length=100)
    contacto = models.ForeignKey(Contacto, related_name='mail', null=True)

    class Meta:
        verbose_name = 'Mail de contacto'
        verbose_name_plural = 'Mails de contactos'

    def __str__(self):
        return self.mail


class ContactoTelefono(models.Model):
    telefono = models.CharField(max_length=12)
    contacto = models.ForeignKey(Contacto, related_name='telefono', null=True)

    class Meta:
        verbose_name = 'Teléfono de contacto'
        verbose_name_plural = 'Teléfonos de contactos'

    def __str__(self):
        return self.telefono
