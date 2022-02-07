from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView

from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin,
    UserPassesTestMixin)

from apps.users.models import Organizacion
from apps.main.models import ArchivoGenerado

from apps.ie.models import (
    Laboratorio, Computadora, Serie, ValidacionVersion,
    Validacion, Requerimiento)
from apps.ie.forms import (
    LaboratorioCreateForm, LaboratorioUpdateForm,
    ComputadoraForm, SerieForm, IEValidacionVersionForm,
    RequerimientoForm, IEValidacionCreateForm, IEValidacionUpdateForm,
    LaboratorioInformeForm, ValidacionInformeForm)


class LaboratorioCreateView(LoginRequiredMixin, CreateView):
    model = Laboratorio
    form_class = LaboratorioCreateForm

    def form_valid(self, form):
        form.instance.poblacion = form.instance.escuela.poblaciones.last()
        form.instance.organizacion = self.request.user.perfil.organizacion
        return super(LaboratorioCreateView, self).form_valid(form)


class LaboratorioDetailView(LoginRequiredMixin, DetailView):
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


class LaboratorioListView(LoginRequiredMixin, ListView):
    model = Laboratorio
    template_name = "ie/laboratorio_list.html"

    def get_context_data(self, **kwargs):
        context = super(LaboratorioListView, self).get_context_data(**kwargs)
        context['organizacion_list'] = Organizacion.objects.all()
        return context

    def get_queryset(self):
        """Para filtrar los laboratorios que corresponden a
        la organización del usuario.
        """
        is_super = self.request.user.is_superuser
        not_org = self.request.user.perfil.organizacion is None
        if (is_super or not_org):
            return Laboratorio.objects.all()
        else:
            return Laboratorio.objects.filter(
                organizacion=self.request.user.perfil.organizacion)


class LaboratorioInformeView(LoginRequiredMixin, FormView):
    form_class = LaboratorioInformeForm
    template_name = 'ie/laboratorio_informe.html'


class LaboratorioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Laboratorio
    template_name = "ie/laboratorio_detail.html"
    form_class = LaboratorioUpdateForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(LaboratorioUpdateView, self).get_context_data(**kwargs)
        context['computadora_form'] = ComputadoraForm(initial={
            'laboratorio': self.object})
        context['serie_form'] = SerieForm()
        return context

    def test_func(self, user):
        """Evista que un usuario que no sea superuser o alguien
        externo a la organización pueda editar los datos.
        """
        is_super = user.is_superuser
        org_valida = user.perfil.organizacion == self.get_object().organizacion
        return (is_super or org_valida)


class ComputadoraCreateView(LoginRequiredMixin, CreateView):
    model = Computadora
    form_class = ComputadoraForm


class SerieCreateView(LoginRequiredMixin, CreateView):
    model = Serie
    form_class = SerieForm


class DashboardView(TemplateView):
    template_name = 'ie/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        try:
            context['archivo_generado'] = ArchivoGenerado.objects.get(nombre='ie_dashboard')
        except ArchivoGenerado.DoesNotExist:
            context['archivo_generado'] = None
        return context


class MapDashboardView(TemplateView):
    template_name = 'ie/dashboard-mapa.html'

    def get_context_data(self, **kwargs):
        context = super(MapDashboardView, self).get_context_data(**kwargs)
        try:
            context['archivo_generado'] = ArchivoGenerado.objects.get(nombre='ie_mapa')
        except ArchivoGenerado.DoesNotExist:
            context['archivo_generado'] = None
        return context


class GeoDashboardView(TemplateView):
    template_name = 'ie/dashboard-geo.html'

    def get_context_data(self, **kwargs):
        context = super(GeoDashboardView, self).get_context_data(**kwargs)
        try:
            context['archivo_generado'] = ArchivoGenerado.objects.get(nombre='ie_geo')
        except ArchivoGenerado.DoesNotExist:
            context['archivo_generado'] = None
        return context


class ValidacionVersionCreateView(LoginRequiredMixin, CreateView):
    model = ValidacionVersion
    template_name = "ie/validacionversion_form.html"
    form_class = IEValidacionVersionForm
    success_url = reverse_lazy('ie_versionvalidacion_add')

    def get_context_data(self, **kwargs):
        context = super(ValidacionVersionCreateView, self).get_context_data(**kwargs)
        context['requerimiento_form'] = RequerimientoForm()
        context['version_list'] = ValidacionVersion.objects.all()
        return context


class RequerimientoCreateView(LoginRequiredMixin, CreateView):
    model = Requerimiento
    form_class = RequerimientoForm
    success_url = reverse_lazy('ie_versionvalidacion_add')

    def form_valid(self, form):
        form.instance.ie_requerimiento_creada_por = self.request.user
        return super(RequerimientoCreateView, self).form_valid(form)


class ValidacionCreateView(LoginRequiredMixin, CreateView):
    model = Validacion
    form_class = IEValidacionCreateForm

    def form_valid(self, form):
        form.instance.organizacion = self.request.user.perfil.organizacion
        return super(ValidacionCreateView, self).form_valid(form)


class IEValidacionDetailView(LoginRequiredMixin, DetailView):
    model = Validacion
    template_name = "ie/validacion_detail.html"


class IEValidacionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Validacion
    form_class = IEValidacionUpdateForm
    template_name = "ie/validacion_detail.html"
    raise_exception = True

    def form_valid(self, form):
        if form.instance.completada:
            form.instance.fecha_fin = datetime.today()
        return super(IEValidacionUpdateView, self).form_valid(form)

    def test_func(self, user):
        """Evista que un usuario que no sea superuser o alguien
        externo a la organización pueda editar los datos.
        """
        validacion = self.get_object()
        is_super = user.is_superuser
        org_valida = user.perfil.organizacion == validacion.organizacion
        return (is_super or org_valida) and not validacion.completada


class IEValidacionInformeView(LoginRequiredMixin, FormView):
    form_class = ValidacionInformeForm
    template_name = 'ie/validacion_informe.html'
