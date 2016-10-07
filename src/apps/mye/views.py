from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CooperanteForm
from .models import Cooperante
from braces.views import LoginRequiredMixin

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