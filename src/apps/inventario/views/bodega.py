from django.shortcuts import render, redirect

from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f
from apps.conta import models as conta_m
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView, FormView

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from apps.conta import forms as conta_f
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin,
    CsrfExemptMixin, JsonRequestResponseMixin)
# Create your views here.


# Tarima

# Listar las tarimas
class TarimaListView(ListView):
    model = inv_m.Tarima
    template_name = 'bodega/tarimas_list.html'


# Crear tarimas
class TarimaCrearCreateView(CreateView):
    model = inv_m.Tarima
    form_class = inv_f.TarimaForm
    template_name = 'bodega/tarimas_add.html'
    success_url = reverse_lazy('tarima_list')


# Actualizar Tarima
class TarimaActualizarUpdateView(UpdateView):
    model = inv_m.Tarima
    form_class = inv_f.TarimaForm
    template_name = 'bodega/tarimas_add.html'
    success_url = reverse_lazy('tarima_list')


# Sector

# Listar las Sectores
class SectoreListarListView(ListView):
    model = inv_m.Sector
    template_name = 'bodega/sectores_list.html'


# Crear Sector
class SectorCrearCreateView(CreateView):
    model = inv_m.Sector
    form_class = inv_f.SectorForm
    template_name = 'bodega/sector_add.html'
    success_url = reverse_lazy('sector_list')


# Actualizar Sector
class SectorActualizarUpdateView(UpdateView):
    model = inv_m.Sector
    form_class = inv_f.TarimaForm
    template_name = 'bodega/sector_add.html'
    success_url = reverse_lazy('sector_list')


# Nivel

# Listar las Niveles
class NivelListarListView(ListView):
    model = inv_m.Nivel
    template_name = 'bodega/nivel_list.html'


# Crear Nivel
class NivelCrearCreateView(CreateView):
    model = inv_m.Nivel
    form_class = inv_f.NivelForm
    template_name = 'bodega/nivel_add.html'
    success_url = reverse_lazy('nivel_list')


# Actualizar Nivel
class NivelActualizarUpdateView(UpdateView):
    model = inv_m.Nivel
    form_class = inv_f.NivelForm
    template_name = 'bodega/nivel_add.html'
    success_url = reverse_lazy('nivel_list')


# Pasillo

# Listar los pasillos
class PasilloListView(ListView):
    model = inv_m.Pasillo
    template_name = 'bodega/pasillo_list.html'


# Crear pasillo
class PasilloCrearCreateView(CreateView):
    model = inv_m.Pasillo
    form_class = inv_f.PasilloForm
    template_name = 'bodega/pasillo_add.html'
    success_url = reverse_lazy('pasillo_list')


# Actualizar Pasillo
class PasilloActualizarUpdateView(UpdateView):
    model = inv_m.Pasillo
    form_class = inv_f.PasilloForm
    template_name = 'bodega/pasillo_add.html'
    success_url = reverse_lazy('pasillo_list')


class SectorDetailView(DetailView):
    model = inv_m.Sector

class BodegaResumenInformeListView(LoginRequiredMixin, FormView):
    """Vista utilizada para listar el resumen de Inventario para Bodega.
    """
    model = conta_m.PrecioEstandar
    template_name = 'inventario/bodega/informebodegaresumen.html'
    form_class = conta_f.ResumenInformeForm

    def get_form(self, form_class=None):
        form = super(BodegaResumenInformeListView, self).get_form(form_class)
        form.fields['tipo_dispositivo'].queryset = self.request.user.tipos_dispositivos.tipos.filter(usa_triage=True)
        return form

class BodegaResumenInformePrintView( TemplateView):
    template_name = 'inventario/bodega/informebodegaresumenprint.html'
