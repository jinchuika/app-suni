#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.utils import timezone

from django.urls import reverse_lazy
from django.shortcuts import reverse
from django.views.generic import DetailView, UpdateView, CreateView, ListView, FormView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


#################################################
# MOVIMIENTOS Y GESTIÓN GENERAL DE DISPOSITIVOS #
#################################################


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
        context['form_falla'] = inv_f.DispositivoFallaCreateForm(initial={'dispositivo': self.object})
        return context


class DispositivoListView(LoginRequiredMixin, FormView):
    """Vista   para obtener los datos de Dispositivos mediante una :class:`Dispositivo`
    Funciona  para recibir los datos de un  'DispositivoForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.Dispositivo
    template_name = 'inventario/dispositivo/dispositivos_list.html'
    form_class = inv_f.DispositivoInformeForm


class SolicitudMovimientoCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Solicitudslug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = TrueMovimiento mediante una :class:`SolicitudMovimiento`
    Funciona  para recibir los datos de un  'SolicitudMovimientoCreateForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SolicitudMovimiento
    template_name = 'inventario/dispositivo/solicitudmovimiento_add.html'
    form_class = inv_f.SolicitudMovimientoCreateForm

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        return super(SolicitudMovimientoCreateView, self).form_valid(form)

    def get_initial(self):
        return {
            'fecha_creacion': None
        }

    def get_form(self, form_class=None):
        form = super(SolicitudMovimientoCreateView, self).get_form(form_class)
        print(self.request.user.tipos_dispositivos.tipos.all())
        form.fields['tipo_dispositivo'].queryset = self.request.user.tipos_dispositivos.tipos.all()
        return form


class SolicitudMovimientoUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para crear `CambioDispositivo` a partir de una `SolicitudMovimiento`"""
    model = inv_m.SolicitudMovimiento
    form_class = inv_f.SolicitudMovimientoUpdateForm
    template_name = 'inventario/dispositivo/solicitudmovimiento_update.html'

    def get_form(self, form_class=None):
        form = super(SolicitudMovimientoUpdateView, self).get_form(form_class)
        form.fields['dispositivos'].widget = forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('inventario_api:api_dispositivo-list'),
            'data-etapa-inicial': self.object.etapa_inicial.id,
            'data-tipo-dispositivo': self.object.tipo_dispositivo.id,
            'data-slug': self.object.tipo_dispositivo.slug,
        })
        form.fields['dispositivos'].queryset = inv_m.Dispositivo.objects.filter(
            etapa=self.object.etapa_inicial,
            tipo=self.object.tipo_dispositivo
        )
        return form

    def form_valid(self, form):
        form.instance.cambiar_etapa(
            lista_dispositivos=form.cleaned_data['dispositivos'],
            usuario=self.request.user
        )
        return super(SolicitudMovimientoUpdateView, self).form_valid(form)


class SolicitudMovimientoDetailView(LoginRequiredMixin, DetailView):
    model = inv_m.SolicitudMovimiento
    template_name = 'inventario/dispositivo/solicitudmovimiento_detail.html'


class SolicitudMovimientoListView(LoginRequiredMixin, ListView):
    model = inv_m.SolicitudMovimiento
    template_name = 'inventario/dispositivo/solicitudmovimiento_list.html'


##########################
# FALLAS DE DISPOSITIVOS #
##########################

class DispositivoFallaCreateView(LoginRequiredMixin, CreateView):
    """Creación de :class:`DispositivoFalla`, no admite el método GET"""
    model = inv_m.DispositivoFalla
    form_class = inv_f.DispositivoFallaCreateForm

    def form_valid(self, form):
        form.instance.reportada_por = self.request.user
        return super(DispositivoFallaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dispositivofalla_update', kwargs={'pk': self.object.id})


class DispositivoFallaUpdateView(LoginRequiredMixin, UpdateView):
    model = inv_m.DispositivoFalla
    form_class = inv_f.DispositivoFallaUpdateForm
    template_name = 'inventario/dispositivo/falla/dispositivofalla_update.html'

    def form_valid(self, form):
        if form.cleaned_data['terminada']:
            form.instance.reparada_por = self.request.user
            form.instance.fecha_fin = timezone.now()
        return super(DispositivoFallaUpdateView, self).form_valid(form)

    def get_success_url(self):
        if self.object.terminada:
            return self.object.get_absolute_url()
        else:
            return reverse_lazy('dispositivofalla_update', kwargs={'pk': self.object.id})


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


class DispositivoTipoCreateView(LoginRequiredMixin, CreateView):
    """Creacion de tipos por medio la :class:`DispositivoTipo`
    """

    model = inv_m.DispositivoTipo
    template_name = 'inventario/dispositivo/dispositivotipo_add.html'
    form_class = inv_f.DispositivoTipoForm

    def get_context_data(self, **kwargs):
        context = super(DispositivoTipoCreateView, self).get_context_data(**kwargs)
        context['dispositivotipo_list'] = inv_m.DispositivoTipo.objects.all()
        return context

    def get_success_url(self):
        return reverse('dispositivo_list')


class DispositivoQRprint(LoginRequiredMixin, DetailView):
    """ Esta vista sirve para imprimir los codigos QR a
    """
    model = inv_m.Dispositivo
    template_name = 'inventario/dispositivo/dispositivo_print.html'
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
