from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CooperanteForm, EscuelaCooperanteForm, ProyectoForm, SolicitudVersionForm, SolicitudForm
from .models import Cooperante, Proyecto, SolicitudVersion, Solicitud
from apps.escuela.models import Escuela
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

class CooperanteCrear(LoginRequiredMixin, CreateView):
	model = Cooperante
	template_name = 'mye/cooperante_form.html'
	form_class = CooperanteForm

class CooperanteDetalle(LoginRequiredMixin, DetailView):
	model = Cooperante
	template_name = 'mye/cooperante.html'

class CooperanteUpdate(LoginRequiredMixin, UpdateView):
	model = Cooperante
	template_name = 'mye/cooperante_form.html'
	form_class = CooperanteForm

class CooperanteList(LoginRequiredMixin, ListView):
	model = Cooperante
	template_name = 'mye/cooperante_list.html'

class ProyectoCrear(LoginRequiredMixin, CreateView):
	model = Proyecto
	template_name = 'mye/proyecto_form.html'
	form_class = ProyectoForm

class ProyectoDetalle(LoginRequiredMixin, DetailView):
	model = Proyecto
	template_name = 'mye/proyecto.html'

class ProyectoUpdate(LoginRequiredMixin, UpdateView):
	model = Proyecto
	template_name = 'mye/proyecto_form.html'
	form_class = ProyectoForm

class ProyectoList(LoginRequiredMixin, ListView):
	model = Proyecto
	template_name = 'mye/proyecto_list.html'

class SolicitudVersionCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	model = SolicitudVersion
	template_name = 'mye/solicitud_version_form.html'
	form_class = SolicitudVersionForm
	permission_required = 'mye.add_solicitud_version'
	redirect_unauthenticated_users = True
	raise_exception = True

class SolicitudVersionDetalle(LoginRequiredMixin, DetailView):
	model = SolicitudVersion
	template_name = 'mye/solicitud_version.html'

class SolicitudCrear(LoginRequiredMixin, CreateView):
	model = Solicitud
	template_name = 'mye/solicitud_form.html'
	form_class = SolicitudForm

	def form_valid(self, form):
		print("hola")
		print(form)
		if form.is_valid():
			print("huwhuwhuw")
		else:
			print(":(")
		return super(SolicitudCrear, self).form_valid(form)

	def form_invalid(self, form):
		print(form.errors)
		return super(SolicitudCrear, self).form_invalid(form)