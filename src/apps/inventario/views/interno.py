from django.shortcuts import reverse, render
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView, View
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, JsonRequestResponseMixin, CsrfExemptMixin, GroupRequiredMixin
)
from django.contrib import messages
from django.db.models import Sum

from apps.escuela import models as escuela_m
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f
from apps.tpe import models as tpe_m
from django import forms
from dateutil.relativedelta import relativedelta
from django.db.models import Q

class InventarioInternoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
	"""Vista para la creación de asignación de dispositivos de inventario interno :class:'InventarioInterno'
	Funciona al recibir datos de un 'InventarioInternoForm' mediante el metodo POST y nos muestra el template
	de visitas mediante el metodo GET.
	"""
	model = inv_m.InventarioInterno
	form_class = inv_f.InventarioInternoForm
	template_name = 'inventario/interno/interno_add.html'
	group_required	= [u"inv_interno", u"inv_admin", u"inv_cc"]

	def get_success_url(self):
		return reverse_lazy('inventariointerno_edit', kwargs={'pk': self.object.id})

	def form_valid(self, form):
		form.instance.creada_por = self.request.user
		form.instance.estado = inv_m.IInternoEstado.objects.get(id=inv_m.IInternoEstado.BR)
		return super(InventarioInternoCreateView, self).form_valid(form)

class InventarioInternoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
	"""Vista para asignar dispositivos al Inventario Interno mediante una :class 'InventarioInterno' 
	"""
	model = inv_m.InventarioInterno
	form_class = inv_f.InventarioInternoForm
	template_name = 'inventario/interno/interno_edit.html'
	group_required	= [u"inv_interno", u"inv_admin", u"inv_cc"]

	def get_context_data(self, *args, **kwargs):
		context = super(InventarioInternoUpdateView, self).get_context_data(*args, **kwargs)
		comentarios_cc = inv_m.IIRevisionComentario.objects.filter(no_asignacion = self.object.id)

		context['dispositivos_form'] = inv_f.InventarioInternoDispositivosForm(initial={'no_asignacion': self.object})
		context['comentario_cc'] = comentarios_cc

		return context

	def get_success_url(self):
		return reverse('inventariointerno_edit', kwargs={'pk': self.object.id})

class InventarioInternoPaqueteUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
	""" Vista para poder asignar dispositivos a un inventario interno """
	model = inv_m.InventarioInterno
	form_class = inv_f.InventarioInternoDispositivosForm
	template_name = 'inventario/interno/asignar_dispositivo.html'
	group_required = [u"inv_interno", u"inv_admin", u"inv_cc"]

	def get_success_url(self):
		return reverse_lazy('inventariointerno_edit', kwargs={'pk': self.object.id})

	def post(self, request, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			return self.form_valid(form, **kwargs)
		else:
			return self.form_invalid(form)
		return super(InventarioInternoPaqueteUpdateView, self).post(request, **kwargs)

	def form_valid(self, form, **kwargs):
		
		no_asignacion = inv_m.InventarioInterno.objects.get(no_asignacion=form.cleaned_data['no_asignacion'])
		indice_actual = no_asignacion.dispositivos.count() + 1
		form.instance.indice = indice_actual
		form.instance.asignado_por = self.request.user

		dispositivo = inv_m.Dispositivo.objects.get(triage=form.cleaned_data['dispositivo'])
		dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(pk=inv_m.DispositivoEtapa.II)
		dispositivo.save()

		return super(InventarioInternoPaqueteUpdateView, self).form_valid(form)

class InventarioInternoDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
	""" Vista para poder ver el detalle de asignaciones ya cerradas """
	model = inv_m.InventarioInterno
	template_name = 'inventario/interno/interno_detail.html'
	group_required = [u"inv_interno", u"inv_admin", u"inv_cc", u"inv_conta", u"tpe_tecnico"]

class InventarioInternoListView(LoginRequiredMixin, GroupRequiredMixin, FormView):
	""" Vista para mostrar la lista de asignaciones de dispositivos de acuerdo a parámetros de búsqueda
	"""
	model = inv_m.IInternoDispositivo
	template_name = 'inventario/interno/interno_list.html'
	form_class = inv_f.InventarioInternoInformeForm
	group_required = [u"inv_interno", u"inv_admin", u"inv_conta",  u"tpe_tecnico"]

class CartaPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
	"""Vista encargada de imprimir la carta de responsabilidad correspondiente"""
	model = inv_m.InventarioInterno
	template_name = 'inventario/interno/carta_print.html'
	group_required = [u"inv_interno", u"inv_admin"]