from django.shortcuts import render
from django.views.generic.edit import CreateView
from braces.views import LoginRequiredMixin
from .forms import FormEscuelaCrear

class EscuelaCrear(LoginRequiredMixin, CreateView):
	template_name = 'escuela/add.html'
	form_class = FormEscuelaCrear