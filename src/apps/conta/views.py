from django.shortcuts import render
from django.urls import reverse_lazy
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin,
    CsrfExemptMixin, JsonRequestResponseMixin)
from django.views.generic import DetailView, ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from apps.conta import models as conta_m
from apps.conta import forms as conta_f


class PeriodoFiscalCreateView(LoginRequiredMixin, CreateView):
    """ Vista   para obtener los datos de Periodo Fiscal mediante una :class:`PeriodoFiscal`
    Funciona  para recibir los datos de un  'PeriodoFiscalForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PeriodoFiscal
    template_name = 'conta/periodo_add.html'
    form_class = conta_f.PeriodoFiscalForm

    def get_success_url(self):
        return reverse_lazy('periodo_list')


class PeriodoFiscalListView(LoginRequiredMixin, ListView):
    """ Vista para Los listados de :class:`PeriodoFiscal`. con sus respectivos datos
    """
    model = conta_m.PeriodoFiscal
    template_name = 'conta/periodo_list.html'


class PeriodoFiscalDetailView(LoginRequiredMixin, DetailView):
    """Vista para detalle de :class:`PeriodoFiscal`.
    """
    model = conta_m.PeriodoFiscal
    template_name = 'conta/periodo_detail.html'


class PeriodoFiscalUpdateView(LoginRequiredMixin, UpdateView):
    """ Vista   para obtener los datos de Periodo Fiscal mediante una :class:`PeriodoFiscal`
    Funciona  para recibir los datos de un  'PeriodoFiscalUpdateForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PeriodoFiscal
    template_name = 'conta/periodo_edit.html'
    form_class = conta_f.PeriodoFiscalUpdateForm

    def get_success_url(self):
        return reverse_lazy('periodo_list')


class PrecioEstandarCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Precio Estandar mediante una :class:`PrecioEstandar`
    Funciona  para recibir los datos de un  'PrecioEstandarForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PrecioEstandar
    template_name = 'conta/precioestandar_add.html'
    form_class = conta_f.PrecioEstandarForm

    def form_valid(self, form):
        periodo_activo = conta_m.PeriodoFiscal.objects.get(actual=True)
        form.instance.creado_por = self.request.user
        form.instance.periodo = periodo_activo
        return super(PrecioEstandarCreateView, self).form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('precioestandar_list')


class PrecioEstandarListView(LoginRequiredMixin, FormView):
    """Vista   para obtener los datos de PrecioEstandar mediante una :class:`PrecioEstandar`
    Funciona  para recibir los datos de un  'PrecioEstandarInformeForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PrecioEstandar
    template_name = 'conta/precioestandar_list.html'
    form_class = conta_f.PrecioEstandarInformeForm
