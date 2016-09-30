from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from .forms import FormEscuelaCrear
from .models import Escuela

class EscuelaCrear(LoginRequiredMixin, GroupRequiredMixin, CreateView):
	group_required = u"Monitoreo"
	template_name = 'escuela/add.html'
	form_class = FormEscuelaCrear

class EscuelaDetail(LoginRequiredMixin, DetailView):
	template_name = 'escuela/detail.html'
	model = Escuela