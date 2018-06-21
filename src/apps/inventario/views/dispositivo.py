#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.views.generic import DetailView, UpdateView, CreateView, ListView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


class AsignacionTecnicoCreateView(LoginRequiredMixin, CreateView):
    """Crea un registro de :class:`AsignacionTecnico`"""
    model = inv_m.AsignacionTecnico
    form_class = inv_f.AsignacionTecnicoForm
    template_name = 'inventario/dispositivo/asignaciontecnico_form.html'


class AsignacionTecnicoListView(LoginRequiredMixin, ListView):
    """Listado de :class:`AsignacionTecnico`"""
    model = inv_m.AsignacionTecnico
    template_name = 'inventario/dispositivo/asignaciontecnico_list.html'


class AsignacionTecnicoUpdateView(LoginRequiredMixin, UpdateView):
    """Edita un registro de :class:`AsignacionTecnico`"""
    model = inv_m.AsignacionTecnico
    form_class = inv_f.AsignacionTecnicoForm
    template_name = 'inventario/dispositivo/asignaciontecnico_form.html'


class DispositivoDetailView(DetailView):
    """
    Esta clase sirve como base para todos los detalles de :class:`Dispositivo`.
    Agrega el formulario para creación de :class:`DipositivoFalla`
    """
    model = inv_m.Dispositivo
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True

    def get_context_data(self, *args, **kwargs):
        context = super(DispositivoDetailView, self).get_context_data(*args, **kwargs)
        context['form_falla'] = inv_f.DispositivoFallaForm(initial={'dispositivo': self.object})
        return context


class DispositivoFallaCreateView(LoginRequiredMixin, CreateView):
    """Creación de :class:`DispositivoFalla`, no admite el método GET"""
    model = inv_m.DispositivoFalla
    form_class = inv_f.DispositivoFallaForm

    def form_valid(self, form):
        form.instance.reportada_por = self.request.user
        return super(DispositivoFallaCreateView, self).form_valid(form)


######################################
# VISTAS ESPECÍFICAS DE DISPOSITIVOS #
######################################


class TecladoUpdateView(LoginRequiredMixin, UpdateView):
    model = inv_m.Teclado
    form_class = inv_f.TecladoForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/teclado/teclado_form.html'


class TecladoDetailView(LoginRequiredMixin, DispositivoDetailView):
    model = inv_m.Teclado
    template_name = 'inventario/dispositivo/teclado/teclado_detail.html'


class MonitorDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Esta clase sirve para ver los detalles de :class:`Monitor`
     mostrando los datos necesarios
    """
    model = inv_m.Monitor
    template_name = 'inventario/dispositivo/monitor/monitor_detail.html'


class MouseDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`Mouse`"""
    model = inv_m.Mouse
    template_name = 'inventario/dispositivo/mouse/mouse_detail.html'


class CPUDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`CPU`"""
    model = inv_m.CPU
    template_name = 'inventario/dispositivo/cpu/cpu_detail.html'


class LaptopDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`Laptop`"""
    model = inv_m.Laptop
    template_name = 'inventario/dispositivo/laptop/laptop_detail.html'


class TabletDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`Tablet`"""
    model = inv_m.Tablet
    template_name = 'inventario/dispositivo/tablet/tablet_detail.html'


class HDDDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`HDD`"""
    model = inv_m.HDD
    template_name = 'inventario/dispositivo/hdd/hdd_detail.html'


class DispositivoRedDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`DispositivoRed`"""
    model = inv_m.DispositivoRed
    template_name = 'inventario/dispositivo/red/red_detail.html'
