from django.db import models
from django.utils.timezone import now

class Empresa(models.Model):
	nombre = models.CharField(max_length=50)
	direccion = models.CharField(max_length=50, null = True, blank=True)
	telefono = models.CharField(max_length=12, null=True, blank=True)
	descripcion = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.nombre

class TipoEvento(models.Model):
	tipo_evento = models.CharField(max_length=50)

	def __str__(self):
		return self.tipo_evento

class Evento(models.Model):
	COLOR_CHOICES=(
		('navy','azul'),
		('aqua','aqua'),
		('purple','Morado'),
		('yellow','Amarillo'),
		('teal','turquesa'),
		('red', 'rojo'),
		('green', 'verde'),
		)
	nombre = models.CharField(max_length=50)
	tipo_de_evento = models.ForeignKey(TipoEvento, on_delete = models.PROTECT)
	direccion = models.CharField(max_length= 100, null=True, blank=True)
	fecha = models.DateField(null=True, blank=True)
	color = models.CharField(default = 'green' ,choices = COLOR_CHOICES, max_length= 10)

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ('nombre',)


class Etiqueta(models.Model):
	COLOR_CHOICES=(
		('navy','azul'),
		('aqua','aqua'),
		('purple','Morado'),
		('yellow','Amarillo'),
		('teal','turquesa'),
		('red', 'rojo'),
		('green', 'verde'),
		)
	etiqueta = models.CharField(max_length=50)
	descripcion = models.TextField(null=True, blank=True)
	color = models.CharField(default = 'purple' ,choices = COLOR_CHOICES, max_length= 10)

	def __str__(self):
		return self.etiqueta

	class Meta:
		ordering = ('etiqueta',)




class Contacto(models.Model):
	nombre = models.CharField(max_length=70)
	apellido = models.CharField(max_length=70)
	direccion = models.CharField(max_length=150, null=True, blank=True)
	etiquetas = models.ManyToManyField(Etiqueta)
	evento = models.ManyToManyField(Evento)
	observacion = models.TextField(null=True, blank=True)
	empresa = models.ForeignKey(Empresa)
	puesto = models.CharField(max_length=75)
	fecha_creacion = models.DateField()

	def __str__(self):
		return self.nombre + " " + self.apellido


class ContactoMail(models.Model):
	mail=models.EmailField(max_length=100)
	contacto= models.ForeignKey(Contacto,related_name='mail')

	def __str__(self):
		return self.mail

class ContactoTelefono(models.Model):
	telefono = models.CharField(max_length=12)
	contacto = models.ForeignKey(Contacto, related_name='telefono')

	def __str__(self):
		return self.telefono
