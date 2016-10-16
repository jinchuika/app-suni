from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin, PermissionRequiredMixin
from .forms import FormEscuelaCrear, ContactoForm, ContactoTelefonoFormSet, ContactoMailFormSet
from .models import Escuela, EscContacto
from .mixins import ContactoContextMixin
from apps.mye.forms import EscuelaCooperanteForm, EscuelaProyectoForm
from apps.mye.models import Cooperante, EscuelaCooperante, Proyecto, EscuelaProyecto

class EscuelaCrear(LoginRequiredMixin, GroupRequiredMixin, CreateView):
	group_required = u"Administración"
	template_name = 'escuela/add.html'
	raise_exception = True
	redirect_unauthenticated_users = True
	form_class = FormEscuelaCrear

class EscuelaDetail(LoginRequiredMixin, DetailView):
	template_name = 'escuela/detail.html'
	model = Escuela

class EscuelaCooperanteUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Escuela
	form_class = EscuelaCooperanteForm
	template_name = 'mye/cooperante_asignacion_escuela.html'
	permission_required = 'mye.change_escuela_cooperante'
	redirect_unauthenticated_users = True
	raise_exception = True

	def get_form(self, *args, **kwargs):
		eliminar = self.request.user.has_perm('mye.delete_escuela_cooperante')
		form = self.form_class(self.get_form_kwargs(), eliminar=eliminar)
		form.initial['cooperante_asignado'] = [c.cooperante for c in EscuelaCooperante.objects.filter(escuela=self.object, activa=True)]
		return form

	def get_success_url(self):
		return reverse('escuela_detail', kwargs={'pk':self.kwargs['pk']})

class EscuelaProyectoUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Escuela
	form_class = EscuelaProyectoForm
	template_name = 'mye/proyecto_asignacion_escuela.html'
	permission_required = 'mye.change_escuela_proyecto'
	redirect_unauthenticated_users = True
	raise_exception = True

	def get_form(self, *args, **kwargs):
		eliminar = self.request.user.has_perm('mye.delete_escuela_proyecto')
		form = self.form_class(self.get_form_kwargs(), eliminar=eliminar)
		form.initial['proyecto_asignado'] = [c.proyecto for c in EscuelaProyecto.objects.filter(escuela=self.object, activa=True)]
		return form

	def get_success_url(self):
		return reverse('escuela_detail', kwargs={'pk':self.kwargs['pk']})

class EscuelaEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = "escuela.change_escuela"
	model = Escuela
	template_name = 'escuela/add.html'
	form_class = FormEscuelaCrear
	raise_exception = True
	redirect_unauthenticated_users = True

class EscContactoCrear(LoginRequiredMixin, ContactoContextMixin, CreateView):
	template_name = 'escuela/contacto.html'
	model = EscContacto
	form_class = ContactoForm
	success_url = 'escuela_add'

	def get_initial(self):
		escuela = get_object_or_404(Escuela, id=self.kwargs.get('id_escuela'))
		return { 'escuela': escuela }

class EscContactoEditar(LoginRequiredMixin, ContactoContextMixin, UpdateView):
	template_name = 'escuela/contacto.html'
	model = EscContacto
	form_class = ContactoForm

	def get_success_url(self):
		return reverse('escuela_detail', kwargs={'pk':self.object.escuela} )