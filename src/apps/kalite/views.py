from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, FormView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin

from apps.kalite import forms as kalite_forms
from apps.kalite.models import Rubrica, Indicador, Visita, Punteo, TipoVisita


class RubricaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Rubrica
    template_name = 'kalite/rubrica_add.html'
    form_class = kalite_forms.RubricaForm

    permission_required = 'kalite.add_rubrica'
    redirect_unauthenticated_users = True
    raise_exception = True
    def form_valid(self, form):
        form.instance.rubrica_creada_por = self.request.user
        return super(RubricaCreateView, self).form_valid(form)

class RubricaDetailView(LoginRequiredMixin, DetailView):
    model = Rubrica
    template_name = 'kalite/rubrica_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RubricaDetailView, self).get_context_data(**kwargs)
        context['indicador_form'] = kalite_forms.IndicadorForm(initial={'rubrica': self.object})
        return context


class RubricaListView(LoginRequiredMixin, ListView):
    model = Rubrica
    template_name = 'kalite/rubrica_list.html'


class IndicadorCreateView(LoginRequiredMixin, CreateView):
    model = Indicador
    form_class = kalite_forms.IndicadorForm
    def form_valid(self, form):
        form.instance.indicador_creada_por = self.request.user
        return super(IndicadorCreateView, self).form_valid(form)

class TipoVisitaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TipoVisita
    form_class = kalite_forms.TipoVisitaForm
    template_name = 'kalite/tipovisita_add.html'
    success_url = reverse_lazy('rubrica_list')

    permission_required = 'kalite.add_tipovisita'
    redirect_unauthenticated_users = True
    raise_exception = True
    def form_valid(self, form):
        form.instance.tipo_visita_creada_por = self.request.user
        return super(TipoVisitaCreateView, self).form_valid(form)


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
        context['grado_form'] = kalite_forms.GradoForm(initial={'visita': self.object})
        return context


class VisitaCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear un registro de :model:`kalite.Visita`.
    Únicamente recibe un `VistaForm` y crea el objeto, por lo que
    no admite el método GET.
    """

    model = Visita
    form_class = kalite_forms.VisitaForm

    def form_valid(self, form):
        form.instance.capacitador = self.request.user
        return super(VisitaCreateView, self).form_valid(form)


class VisitaCalendarView(LoginRequiredMixin, GroupRequiredMixin, FormView):

    """
    Vista para el calendario de KA Lite. Incluye un formulario para filtrar
    por capacitador.
    """

    template_name = 'kalite/calendario.html'
    form_class = kalite_forms.CalendarFilterForm
    group_required = [u"kalite" ]

    def get_form(self, form_class=None):
        form = super(VisitaCalendarView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['capacitador'].queryset = form.fields['capacitador'].queryset.filter(id=self.request.user.id)
            form.fields['capacitador'].empty_label = None
        return form


class VisitaInformeView(LoginRequiredMixin, FormView):

    """Vista para generar un informe de listado de :class:`Visita`
    """

    form_class = kalite_forms.VisitaInformeForm
    template_name = 'kalite/visita_informe.html'


class VisitaDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'kalite/visita_dashboard.html'


class VisitaEscuelaInformeView(LoginRequiredMixin, FormView):

    """Vista para generar un informe de listado de :class:`Visita`
    """

    form_class = kalite_forms.VisitaEscuelaForm
    template_name = 'kalite/escuela_informe.html'
