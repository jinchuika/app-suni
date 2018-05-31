from django.shortcuts import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
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


class DesechoSalidaCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Entrada mediante una :class:`DesechoSalida`
    Funciona  para recibir los datos de un  'DesechoSalidaForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.DesechoSalida
    form_class = inv_f.DesechoSalidaForm
    template_name = 'inventario/desecho/desechosalida_add.html'

    def get_context_data(self, **kwargs):
        context = super(DesechoSalidaCreateView, self).get_context_data(**kwargs)
        context['desechosalida'] = inv_m.DesechoSalida.objects.filter(en_creacion='True')
        return context


class DesechoSalidaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar la :class:`DesechoSalida`. con sus respectios Campos
    """
    model = inv_m.DesechoSalida
    form_class = inv_f.DesechoSalidaUpdateForm
    template_name = 'inventario/desecho/desechosalida_form.html'

    def get_context_data(self, **kwargs):
        context = super(DesechoSalidaUpdateView, self).get_context_data(**kwargs)
        context['DesechoDetalleForm'] = inv_f.DesechoDetalleForm(initial={'desecho': self.object})
        return context

    def get_success_url(self):
        return reverse('desechosalida_update', kwargs={'pk': self.object.id})
