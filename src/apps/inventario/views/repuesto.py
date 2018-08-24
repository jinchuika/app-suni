from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, ListView, FormView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


class RepuestosAsignacionCreateView(LoginRequiredMixin, FormView):
    """Vista   para obtener los datos de Salida mediante una :class:`DispositivoRepuesto`
    Funciona  para recibir los datos de un  'SalidaInventarioForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET."""

    model = inv_m.DispositivoRepuesto
    template_name = 'inventario/repuesto/repuesto_list.html'
    form_class = inv_f.RepuestoForm


class RepuestosDetailView(LoginRequiredMixin, DetailView):
    """Generar detalles de la :class:`Repuesto`   con sus respectivos campos.
    """
    model = inv_m.Repuesto
    template_name = 'inventario/repuesto/repuesto_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RepuestosDetailView, self).get_context_data(**kwargs)
        try:
            buscar = inv_m.DispositivoRepuesto.objects.get(repuesto=self.object)
            context['dispositivo'] = inv_m.Dispositivo.objects.get(triage=buscar.dispositivo)
        except ObjectDoesNotExist as e:
            print("No tiene Dispositivo asignado")
        return context


class RepuestosUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizacion  de la :class:`entrada`   con sus respectivos campos..
    """
    model = inv_m.Repuesto
    template_name = 'inventario/repuesto/repuesto_edit.html'
    form_class = inv_f.RepuestosUpdateForm

    def get_success_url(self):
        return reverse_lazy('repuesto_detail', kwargs={'pk': self.object.id})
