#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.utils import timezone

from django.urls import reverse_lazy
from django.shortcuts import reverse
from django.views.generic import DetailView, UpdateView, CreateView, ListView, FormView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin
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

    def get_success_url(self):
        return reverse('asignaciontecnico_list')


class AsignacionTecnicoListView(LoginRequiredMixin, ListView):
    """Listado de :class:`AsignacionTecnico`"""
    model = inv_m.AsignacionTecnico
    template_name = 'inventario/dispositivo/asignaciontecnico_list.html'


class AsignacionTecnicoUpdateView(LoginRequiredMixin, UpdateView):
    """Edita un registro de :class:`AsignacionTecnico`"""
    model = inv_m.AsignacionTecnico
    form_class = inv_f.AsignacionTecnicoForm
    template_name = 'inventario/dispositivo/asignaciontecnico_form.html'

    def get_success_url(self):
        return reverse('asignaciontecnico_list')


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

    def get_form(self, form_class=None):
        form = super(DispositivoListView, self).get_form(form_class)
        form.fields['tipo'].queryset = self.request.user.tipos_dispositivos.tipos.all().filter(usa_triage=True)
        return form


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
        form.instance.etapa_inicial = inv_m.DispositivoEtapa.objects.get(
            id=inv_m.DispositivoEtapa.AB
            )
        form.instance.etapa_final = inv_m.DispositivoEtapa.objects.get(
            id=inv_m.DispositivoEtapa.TR
            )
        return super(SolicitudMovimientoCreateView, self).form_valid(form)

    def get_initial(self):
        return {
            'fecha_creacion': None
        }

    def get_form(self, form_class=None):
        form = super(SolicitudMovimientoCreateView, self).get_form(form_class)
        tipo_dis = self.request.user.tipos_dispositivos.tipos.all()
        form.fields['tipo_dispositivo'].queryset = self.request.user.tipos_dispositivos.tipos.all()
        return form


class DevolucionCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Solicitudslug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = TrueMovimiento mediante una :class:`SolicitudMovimiento`
    Funciona  para recibir los datos de un  'DevolucionCreateView' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SolicitudMovimiento
    template_name = 'inventario/dispositivo/solicitudmovimiento_add.html'
    form_class = inv_f.DevolucionCreateForm

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        form.instance.devolucion = True
        form.instance.etapa_inicial = inv_m.DispositivoEtapa.objects.get(
            id=inv_m.DispositivoEtapa.TR
            )
        form.instance.etapa_final = inv_m.DispositivoEtapa.objects.get(
            id=inv_m.DispositivoEtapa.AB
            )
        return super(DevolucionCreateView, self).form_valid(form)

    def get_initial(self):
        return {
            'fecha_creacion': None
        }

    def get_form(self, form_class=None):
        form = super(DevolucionCreateView, self).get_form(form_class)
        tipo_dis = self.request.user.tipos_dispositivos.tipos.all()
        form.fields['tipo_dispositivo'].queryset = self.request.user.tipos_dispositivos.tipos.all()
        return form

    def get_success_url(self):        
        if self.object.tipo_dispositivo.usa_triage:
            return reverse('solicitudmovimiento_update', kwargs={'pk': self.object.id})
        else:
            return reverse('solicitudmovimiento_detail', kwargs={'pk': self.object.id})


class SolicitudMovimientoUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para crear `CambioDispositivo` a partir de una `SolicitudMovimiento`"""
    model = inv_m.SolicitudMovimiento
    form_class = inv_f.SolicitudMovimientoUpdateForm
    template_name = 'inventario/dispositivo/solicitudmovimiento_update.html'

    def get_form(self, form_class=None):
        form = super(SolicitudMovimientoUpdateView, self).get_form(form_class)
        estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        form.fields['dispositivos'].widget = forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('inventario_api:api_dispositivo-list'),
            'data-etapa-inicial': self.object.etapa_inicial.id,
            'data-estado-inicial': estado.id,
            'data-tipo-dispositivo': self.object.tipo_dispositivo.id,
            'data-slug': self.object.tipo_dispositivo.slug,
        })
        form.fields['dispositivos'].queryset = inv_m.Dispositivo.objects.filter(
            etapa=self.object.etapa_inicial,
            tipo=self.object.tipo_dispositivo
        )
        return form

    def form_valid(self, form):
        form.instance.autorizada_por = self.request.user
        form.instance.cambiar_etapa(
            lista_dispositivos=form.cleaned_data['dispositivos'],
            usuario=self.request.user
        )
        return super(SolicitudMovimientoUpdateView, self).form_valid(form)


class SolicitudMovimientoDetailView(LoginRequiredMixin, DetailView):
    """ Vista para ver los detalles de la :class:`SolicitudMovimiento`
    """
    model = inv_m.SolicitudMovimiento
    template_name = 'inventario/dispositivo/solicitudmovimiento_detail.html'


class SolicitudMovimientoListView(LoginRequiredMixin, ListView):
    """ Vista para ver la lista  de la :class:`SolicitudMovimiento`
    """
    model = inv_m.SolicitudMovimiento
    template_name = 'inventario/dispositivo/solicitudmovimiento_list.html'


##########################
# FALLAS DE DISPOSITIVOS #
##########################

class DispositivoFallaCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """Creación de :class:`DispositivoFalla`, no admite el método GET"""
    model = inv_m.DispositivoFalla
    form_class = inv_f.DispositivoFallaCreateForm
    group_required = [u"inv_tecnico", u"inv_admin"]

    def form_valid(self, form):
        form.instance.reportada_por = self.request.user
        return super(DispositivoFallaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dispositivofalla_update', kwargs={'pk': self.object.id})


class DispositivoFallaUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """ Vista para actualizar los detalles de la :class:`DispositivoFalla`
    """
    model = inv_m.DispositivoFalla
    form_class = inv_f.DispositivoFallaUpdateForm
    template_name = 'inventario/dispositivo/falla/dispositivofalla_update.html'
    group_required = [u"inv_admin"]

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
    """ Vista para actualizar los detalles de la :class:`Teclado`
    """
    model = inv_m.Teclado
    form_class = inv_f.TecladoForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/teclado/teclado_form.html'

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('teclado_detail', kwargs={'triage': self.object.triage})


class TecladoDetailView(LoginRequiredMixin, DispositivoDetailView):
    """ Vista para ver los detalles de la :class:`Teclado`
    """
    model = inv_m.Teclado
    template_name = 'inventario/dispositivo/teclado/teclado_detail.html'


class MonitorDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Esta clase sirve para ver los detalles de :class:`Monitor`
     mostrando los datos necesarios
    """
    model = inv_m.Monitor
    template_name = 'inventario/dispositivo/monitor/monitor_detail.html'


class MonitorUptadeView(LoginRequiredMixin, UpdateView):
    """ Esta clase sirve para actualizar la  :class:`Monitor`
     mostrando los datos necesarios
    """
    model = inv_m.Monitor
    form_class = inv_f.MonitorForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/monitor/monitor_edit.html'

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('monitor_detail', kwargs={'triage': self.object.triage})


class MouseDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`Mouse`"""
    model = inv_m.Mouse
    template_name = 'inventario/dispositivo/mouse/mouse_detail.html'


class MouseUptadeView(LoginRequiredMixin, UpdateView):
    """ Esta clase sirve para actualizar la  :class:`Mouse`
     mostrando los datos necesarios
    """
    model = inv_m.Mouse
    form_class = inv_f.MouseForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/mouse/mouse_edit.html'

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('mouse_detail', kwargs={'triage': self.object.triage})


class CPUDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`CPU`"""
    model = inv_m.CPU
    template_name = 'inventario/dispositivo/cpu/cpu_detail.html'


class CPUptadeView(LoginRequiredMixin, UpdateView):
    """ Esta clase sirve para actualizar la  :class:`CPU`
     mostrando los datos necesarios
    """
    model = inv_m.CPU
    form_class = inv_f.CPUForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/cpu/cpu_edit.html'

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('cpu_detail', kwargs={'triage': self.object.triage})


class LaptopDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`Laptop`"""
    model = inv_m.Laptop
    template_name = 'inventario/dispositivo/laptop/laptop_detail.html'


class LaptopUptadeView(LoginRequiredMixin, UpdateView):
    """ Esta clase sirve para actualizar la  :class:`Laptop`
     mostrando los datos necesarios
    """
    model = inv_m.Laptop
    form_class = inv_f.LaptopForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/laptop/laptop_edit.html'

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('laptop_detail', kwargs={'triage': self.object.triage})


class TabletDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`Tablet`"""
    model = inv_m.Tablet
    template_name = 'inventario/dispositivo/tablet/tablet_detail.html'


class TabletUptadeView(LoginRequiredMixin, UpdateView):
    """ Esta clase sirve para actualizar la  :class:`Tablet`
     mostrando los datos necesarios
    """
    model = inv_m.Tablet
    form_class = inv_f.TabletForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/tablet/tablet_edit.html'

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('tablet_detail', kwargs={'triage': self.object.triage})


class HDDDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`HDD`"""
    model = inv_m.HDD
    template_name = 'inventario/dispositivo/hdd/hdd_detail.html'


class HDDUptadeView(LoginRequiredMixin, UpdateView):
    """ Esta clase sirve para actualizar la  :class:`HDD`
     mostrando los datos necesarios
    """
    model = inv_m.HDD
    form_class = inv_f.HDDForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/hdd/hdd_edit.html'

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('hdd_detail', kwargs={'triage': self.object.triage})


class DispositivoRedDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`DispositivoRed`"""
    model = inv_m.DispositivoRed
    template_name = 'inventario/dispositivo/red/red_detail.html'


class DispositivoRedUptadeView(LoginRequiredMixin, UpdateView):
    """ Vista actualizar los  dispositivos tipo :class:`DispositivoRed`
    """
    model = inv_m.DispositivoRed
    form_class = inv_f.DispositivoRedForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/red/red_edit.html'

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('red_detail', kwargs={'triage': self.object.triage})


class DispositivoAccessPointDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`DispositivoRed`"""
    model = inv_m.AccessPoint
    template_name = 'inventario/dispositivo/ap/ap_detail.html'


class DispositivoAccessPointUptadeView(LoginRequiredMixin, UpdateView):
    """ Vista actualizar los  dispositivos tipo :class:`DispositivoRed`
    """
    model = inv_m.AccessPoint
    form_class = inv_f.DispositivoAccessPointForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/ap/ap_edit.html'

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('ap_detail', kwargs={'triage': self.object.triage})


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


class DispositivoQRprint(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """ Vista encargada de imprimir los codigos qr de  la class `Dispositivo`
    """
    model = inv_m.Dispositivo
    template_name = 'inventario/dispositivo/dispositivo_print.html'
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    group_required = [u"inv_bodega", u"inv_admin"]


class DispositivosTarimaListView(LoginRequiredMixin, FormView):
    """ Vista Encargada de crear los informes de  las Dispositivo obteniendo los datos
    desde el DRF
    """
    model = inv_m.Dispositivo
    template_name = 'inventario/dispositivo/dispositivo_tarima_list.html'
    form_class = inv_f.DispositivosTarimaFormNew


class DispositivosTarimaQr(LoginRequiredMixin, DetailView):
    """Vista encargada de imprimir la lista de codigos qr generada por `DispositivosTarimaListView`
    """
    model = inv_m.Tarima
    template_name = 'inventario/entrada/imprimir_qr.html'

    def get_context_data(self, **kwargs):
        tarima = self.request.GET['tarima']
        tipo = self.request.GET['tipo']
        tarima_print = inv_m.Dispositivo.objects.filter(
            tarima=tarima,
            tipo=tipo,
            estado=inv_m.DispositivoEstado.PD,
            etapa=inv_m.DispositivoEtapa.AB).order_by('triage')

        context = super(DispositivosTarimaQr, self).get_context_data(**kwargs)
        context['dispositivo_qr'] = tarima_print

        return context
