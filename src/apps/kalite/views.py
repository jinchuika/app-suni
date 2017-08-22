from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, FormView

from braces.views import LoginRequiredMixin

from apps.kalite.forms import RubricaForm, IndicadorForm
from apps.kalite.models import Rubrica, Indicador


class RubricaCreateView(LoginRequiredMixin, CreateView):
    model = Rubrica
    template_name = 'kalite/rubrica_add.html'
    form_class = RubricaForm


class RubricaDetailView(LoginRequiredMixin, DetailView):
    model = Rubrica
    template_name = 'kalite/rubrica_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RubricaDetailView, self).get_context_data(**kwargs)
        context['indicador_form'] = IndicadorForm(initial={'rubrica': self.object})
        return context


class RubricaListView(LoginRequiredMixin, ListView):
    model = Rubrica
    template_name = 'kalite/rubrica_list.html'


class IndicadorCreateView(LoginRequiredMixin, CreateView):
    model = Indicador
    form_class = IndicadorForm
