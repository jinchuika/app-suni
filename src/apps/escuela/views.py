from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin, PermissionRequiredMixin
from .forms import FormEscuelaCrear, ContactoForm, ContactoTelefonoFormSet, ContactoMailFormSet
from .models import Escuela, EscContacto
from .mixins import ContactoContextMixin
from apps.mye.forms import EscuelaCooperanteForm

class EscuelaCrear(LoginRequiredMixin, GroupRequiredMixin, CreateView):
	group_required = u"Administración"
	template_name = 'escuela/add.html'
	raise_exception = True
	redirect_unauthenticated_users = True
	form_class = FormEscuelaCrear

class EscuelaDetail(LoginRequiredMixin, DetailView):
	template_name = 'escuela/detail.html'
	model = Escuela

	def get_context_data(self, **kwargs):
		context = super(EscuelaDetail, self).get_context_data(**kwargs)
		context['form_cooperante'] = EscuelaCooperanteForm(instance=self.object)
		return context

class EscuelaCooperanteUpdate(LoginRequiredMixin, UpdateView):
	model = Escuela
	form_class = EscuelaCooperanteForm

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
	success_url = 'escuela_add'
