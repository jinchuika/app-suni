from __future__ import unicode_literals
from apps.users.models import Perfil
from django.db import models
import datetime

#Equipo
class Equipo(models.Model):
	nombre_equipo = models.CharField(max_length= 70)
	
	#métodos
	def get_cant_entradas(self, ini="2000-01-01", out=datetime.date.today()):
		cantidad_ingresos = 0
		entrada_list = Entrada.objects.filter(equipo = self, fecha__range=(ini,out))
		for salida in entrada_list:
			cantidad_ingresos += 1
		return cantidad_ingresos

	def get_entradas(self, ini="2000-01-01", out=datetime.date.today()):
		cantidad_ingresada = 0
		entrada_list = Entrada.objects.filter(equipo = self, fecha__range=(ini, out))
		for entrada in entrada_list:
			cantidad_ingresada += entrada.cantidad
		return cantidad_ingresada
	
	total_ingreso = property(get_entradas)
	cantidad_ingreso = property(get_cant_entradas)

	def get_cant_salidas(self, ini="2000-01-01", out=datetime.date.today()):
		cantidad_egresos = 0
		salida_query = Salida.objects.filter(fecha__range=(ini, out))
		salidaequipo_query = SalidaEquipo.objects.filter(salida__fecha__range=(ini, out), equipo = self)
		for salida in salidaequipo_query:
			cantidad_egresos += 1
		return cantidad_egresos

	def get_salidas(self, ini="2000-01-01", out=datetime.date.today()):
		cantidad_egresada = 0
		salida_query = Salida.objects.filter(fecha__range = (ini, out))
		salidaequipo_query = SalidaEquipo.objects.filter(salida__in=salida_query, equipo = self)
		for salida in salidaequipo_query:
			cantidad_egresada += salida.cantidad

		return cantidad_egresada
	
	total_egreso = property(get_salidas)
	cantidad_egreso = property(get_cant_salidas)
	

	def get_existencia(self):
		existencia = self.get_entradas() - self.get_salidas()
		

		return existencia
	#nueva propiedad
	existencia = property(get_existencia)
	class Meta:
		verbose_name='Equipo'
		verbose_name_plural='Equipo'

	def __str__(self):
		return self.nombre_equipo

#tipo de proveedor
class TipoProveedor(models.Model):
	#atributos
	tipo_de_proveedor = models.CharField(max_length=15)
	class Meta:
		verbose_name='Tipo de Proveedor'
		verbose_name_plural='Tipos de Proveedores'

	#metodos
	def __str__(self):
		return self.tipo_de_proveedor

#estado del equipo
class EstadoEquipo(models.Model):
	#atributos
	estado_del_equipo = models.CharField(max_length=10)
	class Meta:
		verbose_name='Estado del Equipo'
		verbose_name_plural='Estados del Equipo'
	#metodos
	def __str__(self):
		return self.estado_del_equipo

#ripo de salida
class TipoSalida(models.Model):
	#atributos
	tipo_de_salida = models.CharField(max_length=15)
	class Meta:
		verbose_name='Tipo de Salida'
		verbose_name_plural='Tipos de Salidas'
	#metodos
	def __str__(self):
		return self.tipo_de_salida

#tipo de entrada
class TipoEntrada(models.Model):
	#atributos
	tipo_de_entrada= models.CharField(max_length=15)
	class Meta:
		verbose_name='Tipo de Entrada'
		verbose_name_plural='Tipos de Entrada'

	#metodos
	def __str__(self):
		return str(self.tipo_de_entrada)


#Proveedor
class Proveedor(models.Model):
	#atributos
	nombre = models.CharField(max_length=75)
	tipo_de_proveedor = models.ForeignKey(TipoProveedor, on_delete=models.PROTECT)
	direccion = models.CharField(max_length=50)
	telefono = models.IntegerField()
	class Meta:
		verbose_name='Proveedor'
		verbose_name_plural='Proveedores'
	#metodos
	def __str__(self):
		return self.nombre

#Entrada
class Entrada(models.Model):
	#atributos
	equipo = models.ForeignKey(Equipo, on_delete= models.PROTECT, related_name='entradas')
	estado = models.ForeignKey(EstadoEquipo, on_delete = models.PROTECT)
	proveedor= models.ForeignKey(Proveedor, on_delete = models.PROTECT)
	tipo_entrada = models.ForeignKey(TipoEntrada, on_delete = models.PROTECT)
	cantidad = models.IntegerField()
	fecha= models.DateField()
	precio = models.DecimalField(max_digits=7, decimal_places=2, null = True, blank = True )
	factura = models.IntegerField(null = True, blank = True)
	observacion = models.TextField(null = True, blank = True)
	class Meta:
		verbose_name='Entrada'
		verbose_name_plural='Entradas'

	#metodos

	def __str__(self):
		return str(self.id) + " " + str(self.equipo) + " (" + str(self.fecha) + ")"


#salida
class Salida(models.Model):
	#atributos
	tecnico= models.ForeignKey(Perfil, on_delete = models.PROTECT)
	fecha= models.DateField()
	tipo_salida = models.ForeignKey(TipoSalida, on_delete = models.PROTECT)
	observacion = models.TextField(null = True, blank = True)
	class Meta:
		verbose_name='Salida'
		verbose_name_plural='Salidas'
	#metodos
	def __str__(self):
		return "id: " + str(self.id) + " - Técnico: " + str(self.tecnico) + " - Fecha: " + str(self.fecha) 


class SalidaEquipo(models.Model):
	salida = models.ForeignKey(Salida, related_name='salida', null=True)
	equipo = models.ForeignKey(Equipo, on_delete= models.PROTECT, related_name='equipo')
	cantidad = models.IntegerField()

	def __str__(self):
		return str(self.equipo) + " " + str(self.cantidad)