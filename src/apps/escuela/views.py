from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin, PermissionRequiredMixin
from .forms import FormEscuelaCrear, ContactoForm, ContactoTelefonoFormSet, ContactoMailFormSet
from .models import Escuela, EscContacto
from .mixins import ContactoContextMixin

class EscuelaCrear(LoginRequiredMixin, GroupRequiredMixin, CreateView):
	group_required = u"Administración"
	template_name = 'escuela/add.html'
	raise_exception = True
	redirect_unauthenticated_users = True
	form_class = FormEscuelaCrear

class EscuelaDetail(LoginRequiredMixin, DetailView):
	template_name = 'escuela/detail.html'
	model = Escuela

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

class EscContactoEditar(LoginRequiredMixin, ContactoContextMixin, UpdateView):
	template_name = 'escuela/contacto.html'
	model = EscContacto
	form_class = ContactoForm
	success_url = 'escuela_add'
	
