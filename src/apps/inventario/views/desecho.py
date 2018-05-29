from django.shortcuts import reverse
from django.views.generic import CreateView, DetailView, ListView
from braces.views import (
    LoginRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


class DesechoEmpresaCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Entrada mediante una :class:`DesechoEmpresa`
    Funciona  para recibir los datos de un  'DesechoEmpresaForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.DesechoEmpresa
    form_class = inv_f.DesechoEmpresaForm
    template_name = 'inventario/desecho/desechoempresa_form.html'


class DesechoEmpresaDetailView(LoginRequiredMixin, DetailView):
    """Para generar detalles de la :class:`DesechoEmpresa`   con sus respectivos campos.
    """
    model = inv_m.DesechoEmpresa
    template_name = 'inventario/desecho/desechoempresa_detail.html'


class DesechoEmpresaListView(LoginRequiredMixin, ListView):
    """Listado del :class:`DesechoEmpresa` con sus respectivos datos
    """
    model = inv_m.DesechoEmpresa
    template_name = 'inventario/desecho/desechoempresa_list.html'
