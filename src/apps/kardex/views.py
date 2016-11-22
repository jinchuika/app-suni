from django.shortcuts import render
from apps.kardex.models import *
from apps.kardex.forms import *
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from .mixins import SalidaContextMixin
import json
from datetime import date


class Equipolog(LoginRequiredMixin, CreateView):
	model = Equipo
	form_class = FormularioEquipo
	template_name = "kardex/equipo.html"
	success_url = reverse_lazy('kardex_equipo')
	def get_context_data(self, **kwargs):
	    context = super(Equipolog, self).get_context_data(**kwargs)
	    context['lista'] = self.model.objects.all()
	    return context
	    
def informe_general(request, ini, out):
	if ini == "all" or out =="all":
		ini = "2014-01-01"
		out = date.today()
	equipo_list = Equipo.objects.all()
	lista_vacia = []
	for equipo in equipo_list:
		if equipo.get_cant_entradas( ini, out) !=0:
			lista_vacia.append({'nombre':str(equipo), 'cantidad_ingresos':equipo.get_cant_entradas( ini, out), 
				'cantidad_egresos': equipo.get_cant_salidas( ini, out), 'ingreso':equipo.get_entradas( ini, out), 
				'egreso': equipo.get_salidas( ini, out), 'diferencia' : equipo.get_entradas(ini, out)-equipo.get_salidas(ini, out), 
				'existencia_actual': equipo.get_existencia()})
	return HttpResponse(json.dumps({'properties': lista_vacia,}))


class EquipoEntrada(LoginRequiredMixin, DetailView):
	model = Equipo
	def get(self, request, **kwargs):
		lista_entrada = Entrada.objects.filter(equipo = self.get_object())
		lista_vacia = []
		for ingreso in lista_entrada:
			lista_vacia.append({'id':ingreso.id, 'fecha':str(ingreso.fecha), 'cantidad': ingreso.cantidad, 'observacion':ingreso.observacion})
		return HttpResponse(
				json.dumps({
					"tablainf": lista_vacia,
					})
				)

class EquipoSalida(LoginRequiredMixin, DetailView):
	model = Equipo
	def get(self, request, **kwargs):
		lista_salida = Salida.objects.filter()

		lista2 = SalidaEquipo.objects.filter(equipo = self.get_object())
		lista_vacia = []
		for egreso in lista2:
			lista_vacia.append({'id':egreso.id, 'tecnico':str(egreso.salida.tecnico), 'fecha': str(egreso.salida.fecha), 'cantidad': egreso.cantidad})
		return HttpResponse(
			json.dumps({
				"tablainf" : lista_vacia,
				})
			)
	


#entrada del equipo
class EntradaCreate(LoginRequiredMixin, CreateView):
	model = Entrada
	form_class = FormularioEntrada
	template_name = "kardex/entrada.html"
	success_url = reverse_lazy('kardex_equipo')
	
	def get_context_data(self, **kwargs):
		context = super(EntradaCreate, self).get_context_data(**kwargs)
		context['formulario'] = FormularioEntradaInforme
		return context

	def form_valid(self, form):
		self.object = form.save(commit = False)
		precio = self.object.precio
		if precio is not None and precio <= 0:
			return self.form_invalid(form)
		else:
			self.object.save()
			return super(EntradaCreate, self).form_valid(form)

def get_informe_entradas(request, tipo, ini, out):
	if ini == "all" and out == "all" and tipo == "all":
		lista_entrada = Entrada.objects.filter()
	else:
		if tipo == "all":
			lista_entrada = Entrada.objects.filter(fecha__range=(ini, out))
		else:
			if ini == "all" and out == "all":
				lista_entrada = Entrada.objects.filter(tipo_entrada__id = tipo)	
			else:
				lista_entrada = Entrada.objects.filter(tipo_entrada__id = tipo, fecha__range=(ini, out))	
	lista_vacia = []
	if tipo == "2":
		for ingreso in lista_entrada:
			lista_vacia.append({'id':ingreso.id, 'equipo':str(ingreso.equipo), 'tipo':str(ingreso.tipo_entrada), 'fecha':str(ingreso.fecha), 'cantidad': ingreso.cantidad, 'precio':str(ingreso.precio), 'factura':str(ingreso.factura)})
	else:
		for ingreso in lista_entrada:
			lista_vacia.append({'id':ingreso.id, 'equipo':str(ingreso.equipo), 'tipo':str(ingreso.tipo_entrada), 'fecha':str(ingreso.fecha), 'cantidad': ingreso.cantidad})

	return HttpResponse(
			json.dumps({
				"tablainf": lista_vacia,
				})
			)

#Salida del equipo
class SalidaCreate(LoginRequiredMixin, SalidaContextMixin, CreateView):
	model = Salida
	form_class = FormularioSalida
	template_name = "kardex/salida.html"
	success_url = reverse_lazy('kardex_equipo')
	def get_context_data(self, **kwargs):
	    context = super(SalidaCreate, self).get_context_data(**kwargs)
	    context['formulario'] = FormularioSalidaInforme
	    return context

def get_informe_salidas(request, tecnico, ini, out):
	if tecnico == "all":
		lista_entrada = SalidaEquipo.objects.filter(salida__fecha__range=(ini, out))
	else:	
		lista_entrada = SalidaEquipo.objects.filter(salida__tecnico__id = tecnico, salida__fecha__range=(ini, out))
	
	lista_vacia = []
	for salida in lista_entrada:
		lista_vacia.append({'id':salida.id, 'tecnico':str(salida.salida.tecnico), 'fecha': str(salida.salida.fecha), 'equipo':str(salida.equipo), 'cantidad': salida.cantidad})
	
	return HttpResponse(
			json.dumps({
				"tablainf": lista_vacia, 
				})
			)

	


class ProveedorCreate(LoginRequiredMixin, CreateView):
	model = Proveedor
	form_class = FormularioProveedor
	template_name = "kardex/proveedor.html"
	success_url = reverse_lazy('kardex_proveedor')