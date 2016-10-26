from django.views.generic.edit import CreateView
from braces.views import LoginRequiredMixin
from apps.cyd.forms import CursoForm
from apps.cyd.mixins import CursoMixin
from apps.cyd.models import Curso


class CursoCrear(LoginRequiredMixin, CursoMixin, CreateView):
    model = Curso
    template_name = 'cyd/curso_add.html'
    form_class = CursoForm
    success_url = 'escuela_add'
