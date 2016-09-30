from __future__ import unicode_literals
from apps.users.models import Perfil
from django.db import models

#Equipo
class Equipo(models.Model):
	nombre_equipo = models.CharField(max_length= 70)
	
	#métodos
	def get_entradas(self):
		cantidad_ingresada = 0
		entrada_list = Entrada.objects.filter(equipo = self)
		for entrada in entrada_list:
			cantidad_ingresada += entrada.cantidad

		return cantidad_ingresada
	
	total_ingreso = property(get_entradas)

	def get_salidas(self):
		cantidad_egresada = 0
		entrada_list = Salida.objects.filter(equipo = self)
		for entrada in entrada_list:
			cantidad_egresada += entrada.cantidad

		return cantidad_egresada
	
	total_egreso = property(get_salidas)





	def get_existencia(self):
		existencia = self.total_ingreso - self.total_egreso
		

		return existencia
	#nueva propiedad
	existencia = property(get_existencia)

	def __str__(self):
		return self.nombre_equipo

#tipo de proveedor
class TipoProveedor(models.Model):
	#atributos
	tipo_de_proveedor = models.CharField(max_length=15)

	#metodos
	def __str__(self):
		return self.tipo_de_proveedor

#estado del equipo
class EstadoEquipo(models.Model):
	#atributos
	estado_del_equipo = models.CharField(max_length=10)

	#metodos
	def __str__(self):
		return self.estado_del_equipo

#ripo de salida
class TipoSalida(models.Model):
	#atributos
	tipo_de_salida = models.CharField(max_length=15)

	#metodos
	def __str__(self):
		return self.tipo_de_salida

#tipo de entrada
class TipoEntrada(models.Model):
	#atributos
	tipo_de_entrada= models.CharField(max_length=15)

	#metodos
	def __str__(self):
		return self.tipo_de_entrada


#Proveedor
class Proveedor(models.Model):
	#atributos
	nombre = models.CharField(max_length=75)
	tipo_de_proveedor = models.ForeignKey(TipoProveedor, on_delete=models.PROTECT)
	direccionn = models.CharField(max_length=50)
	telefono = models.IntegerField()

	#metodos
	def __str__(self):
		return self.nombre

#Entrada
class Entrada(models.Model):
	#atributos
	equipo = models.ForeignKey(Equipo, on_delete= models.PROTECT)
	proveedor= models.ForeignKey(Proveedor, on_delete = models.PROTECT)
	fecha= models.DateField()
	estado = models.ForeignKey(EstadoEquipo, on_delete = models.PROTECT)
	tipo_entrada = models.ForeignKey(TipoEntrada, on_delete = models.PROTECT)
	cantidad = models.IntegerField()
	precio = models.DecimalField(max_digits=7, decimal_places=2, null = True, blank = True )
	factura = models.IntegerField(null = True, blank = True)
	observacion = models.TextField(null = True, blank = True)


	#metodos

	def __str__(self):
		return str(self.id) + " " + str(self.equipo) + " (" + str(self.fecha) + ")"


#salida
class Salida(models.Model):
	#atributos
	equipo = models.ForeignKey(Equipo, on_delete= models.PROTECT)
	cantidad = models.IntegerField()
	tecnico= models.ForeignKey(Perfil, on_delete = models.PROTECT)
	fecha= models.DateField()
	estado = models.ForeignKey(EstadoEquipo, on_delete = models.PROTECT)
	tipo_salida = models.ForeignKey(TipoSalida, on_delete = models.PROTECT)
	observacion = models.TextField(null = True, blank = True)
	no_entrada = models.ForeignKey(Entrada, on_delete = models.PROTECT, null = True, blank = True)

	#metodos
	def __str__(self):
		return str(self.id) + " " + str(self.equipo) + " (" + str(self.fecha) + ")"
