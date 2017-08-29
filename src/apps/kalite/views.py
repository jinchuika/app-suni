from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from apps.kalite.forms import (
    RubricaForm, IndicadorForm, VisitaForm, TipoVisitaForm,
    GradoForm)
from apps.kalite.models import Rubrica, Indicador, Visita, Punteo, TipoVisita


class RubricaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Rubrica
    template_name = 'kalite/rubrica_add.html'
    form_class = RubricaForm

    permission_required = 'kalite.add_rubrica'
    redirect_unauthenticated_users = True
    raise_exception = True


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


class TipoVisitaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TipoVisita
    form_class = TipoVisitaForm
    template_name = 'kalite/tipovisita_add.html'
    success_url = reverse_lazy('rubrica_list')

    permission_required = 'kalite.add_tipovisita'
    redirect_unauthenticated_users = True
    raise_exception = True


class TipoVisitaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TipoVisita
    template_name = 'kalite/tipovisita_list.html'

    permission_required = 'kalite.add_tipovisita'
    redirect_unauthenticated_users = True
    raise_exception = True


class VisitaDetailView(LoginRequiredMixin, DetailView):
    model = Visita
    template_name = 'kalite/visita_detail.html'

    def get_context_data(self, **kwargs):
        context = super(VisitaDetailView, self).get_context_data(**kwargs)
        context['notas_list'] = Punteo.notas()
        context['grado_form'] = GradoForm(initial={'visita': self.object})
        return context


class VisitaCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear un registro de :model:`kalite.Visita`.
    Únicamente recibe un `VistaForm` y crea el objeto, por lo que
    no admite el método GET.
    """

    model = Visita
    form_class = VisitaForm

    def form_valid(self, form):
        form.instance.capacitador = self.request.user
        return super(VisitaCreateView, self).form_valid(form)


class VisitaCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'kalite/calendario.html'
