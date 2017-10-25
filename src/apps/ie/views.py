from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from apps.users.models import Organizacion

from apps.ie.models import (
    Laboratorio, Computadora, Serie, ValidacionVersion,
    Validacion, Requerimiento)
from apps.ie.forms import (
    LaboratorioCreateForm, LaboratorioUpdateForm,
    ComputadoraForm, SerieForm, IEValidacionVersionForm,
    RequerimientoForm)


class LaboratorioCreateView(CreateView):
    model = Laboratorio
    form_class = LaboratorioCreateForm

    def form_valid(self, form):
        form.instance.poblacion = form.instance.escuela.poblaciones.last()
        form.instance.organizacion = self.request.user.perfil.organizacion
        return super(LaboratorioCreateView, self).form_valid(form)


class LaboratorioDetailView(DetailView):
    model = Laboratorio
    template_name = "ie/laboratorio_detail.html"

    def get_context_data(self, **kwargs):
        context = super(LaboratorioDetailView, self).get_context_data(**kwargs)
        context['computadora_form'] = ComputadoraForm(initial={
            'laboratorio': self.object})

        # filtrar las computadoras de este laboratorio
        context['serie_form'] = SerieForm()
        computadora_queryset = context['serie_form'].fields['computadora'].queryset
        computadora_queryset = computadora_queryset.filter(laboratorio=self.object)
        context['serie_form'].fields['computadora'].queryset = computadora_queryset
        return context


class LaboratorioListView(ListView):
    model = Laboratorio
    template_name = "ie/laboratorio_list.html"

    def get_context_data(self, **kwargs):
        context = super(LaboratorioListView, self).get_context_data(**kwargs)
        context['organizacion_list'] = Organizacion.objects.all()
        return context


class LaboratorioUpdateView(UpdateView):
    model = Laboratorio
    template_name = "ie/laboratorio_detail.html"
    form_class = LaboratorioUpdateForm

    def get_context_data(self, **kwargs):
        context = super(LaboratorioUpdateView, self).get_context_data(**kwargs)
        context['computadora_form'] = ComputadoraForm(initial={
            'laboratorio': self.object})
        context['serie_form'] = SerieForm()
        return context


class ComputadoraCreateView(CreateView):
    model = Computadora
    form_class = ComputadoraForm


class SerieCreateView(CreateView):
    model = Serie
    form_class = SerieForm


class DashboardView(TemplateView):
    template_name = 'ie/dashboard.html'


class MapDashboardView(TemplateView):
    template_name = 'ie/dashboard-mapa.html'


class GeoDashboardView(TemplateView):
    template_name = 'ie/dashboard-geo.html'


class ValidacionVersionCreateView(CreateView):
    model = ValidacionVersion
    template_name = "ie/validacionversion_form.html"
    form_class = IEValidacionVersionForm
    success_url = reverse_lazy('ie_versionvalidacion_add')

    def get_context_data(self, **kwargs):
        context = super(ValidacionVersionCreateView, self).get_context_data(**kwargs)
        context['requerimiento_form'] = RequerimientoForm()
        context['version_list'] = ValidacionVersion.objects.all()
        return context


class RequerimientoCreateView(CreateView):
    model = Requerimiento
    form_class = RequerimientoForm
    success_url = reverse_lazy('ie_versionvalidacion_add')


class ValidacionCreateView(CreateView):
    model = Validacion
