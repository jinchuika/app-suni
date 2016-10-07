from django.shortcuts import render
from django.views.generic.edit import CreateView
from braces.views import LoginRequiredMixin
from .forms import CursoForm
from .mixins import CursoMixin
from .models import Curso

class CursoCrear(LoginRequiredMixin, CursoMixin, CreateView):
	model = Curso
	template_name = 'cyd/curso_add.html'
	form_class = CursoForm
	success_url = 'escuela_add'