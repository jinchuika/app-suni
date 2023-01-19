#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.utils import timezone

from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import reverse
from django.views.generic import DetailView, UpdateView, CreateView, ListView, FormView
from django.db.models import Q
from django.db.models import Sum
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin
)
from apps.beqt import models as beqt_m
from apps.beqt import forms as beqt_f

from apps.inventario import models as inv_m


#################################################
# MOVIMIENTOS Y GESTIÓN GENERAL DE DISPOSITIVOS #
#################################################

class AsignacionTecnicoCreateView(LoginRequiredMixin, CreateView):
    """Crea un registro de :class:`AsignacionTecnico`"""
    model = beqt_m.AsignacionTecnico
    form_class = beqt_f.AsignacionTecnicoForm
    template_name = 'beqt/dispositivo/asignaciontecnico_form.html'

    def get_success_url(self):
        return reverse('asignaciontecnico_list')


class AsignacionTecnicoListView(LoginRequiredMixin, ListView):
    """Listado de :class:`AsignacionTecnico`"""
    model = beqt_m.AsignacionTecnico
    template_name = 'beqt/dispositivo/asignaciontecnico_list.html'


class AsignacionTecnicoUpdateView(LoginRequiredMixin, UpdateView):
    """Edita un registro de :class:`AsignacionTecnico`"""
    model = beqt_m.AsignacionTecnico
    form_class = beqt_f.AsignacionTecnicoForm
    template_name = 'beqt/dispositivo/asignaciontecnico_form.html'

    """def form_valid(self, form):
        print(form.instance.usuario)
        form.instance.usuario = form.instance.usuario
        form.instance.creada_por = self.request.user
        return super(AsignacionTecnicoUpdateView, self).form_valid(form)"""


    def get_success_url(self):
        return reverse('asignaciontecnico_list')


class DispositivoDetailView(DetailView):
    """
    Esta clase sirve como base para todos los detalles de :class:`Dispositivo`.
    Agrega el formulario para creación de :class:`DipositivoFalla`
    """
    model = beqt_m.DispositivoBeqt
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True

    def get_context_data(self, *args, **kwargs):
        context = super(DispositivoDetailView, self).get_context_data(*args, **kwargs)
        context['form_falla'] = beqt_f.DispositivoFallaCreateForm(initial={'dispositivo': self.object})
        return context


class DispositivoListView(LoginRequiredMixin, FormView):
    """Vista   para obtener los datos de Dispositivos mediante una :class:`Dispositivo`
    Funciona  para recibir los datos de un  'DispositivoForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = beqt_m.DispositivoBeqt
    template_name = 'beqt/dispositivo/dispositivos_list.html'
    form_class = beqt_f.DispositivoInformeForm

    def get_form(self, form_class=None):
        form = super(DispositivoListView, self).get_form(form_class)
        form.fields['tipo'].queryset = self.request.user.tipos_dispositivos_beqt.tipos.all().filter(usa_triage=True)
        return form


class SolicitudMovimientoCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Solicitudslug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = TrueMovimiento mediante una :class:`SolicitudMovimiento`
    Funciona  para recibir los datos de un  'SolicitudMovimientoCreateForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = beqt_m.SolicitudMovimientoBeqt
    template_name = 'beqt/dispositivo/solicitudmovimiento_add.html'
    form_class = beqt_f.SolicitudMovimientoCreateForm
    group_required = []

    def form_valid(self, form):
        cantidad = form.cleaned_data['cantidad']
        tipo_dispositivo = form.cleaned_data['tipo_dispositivo']        
        no_salida = form.cleaned_data['no_salida']      

        if cantidad <= 0:
            form.add_error('cantidad', 'La cantidad debe ser mayor a 0')
            return self.form_invalid(form)       

        etapa_transito = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.AB)
        estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        validar_dispositivos = beqt_m.DispositivoTipoBeqt.objects.get(tipo=tipo_dispositivo)
        numero_dispositivos = beqt_m.DispositivoBeqt.objects.filter(tipo=validar_dispositivos, etapa=etapa_transito, estado=estado).count()
               
        if(cantidad > numero_dispositivos):
            form.add_error('cantidad', 'No  hay suficientes dipositivos para satifacer la solicitud')
            return self.form_invalid(form)
        else:
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
        form.fields['tipo_dispositivo'].queryset = self.request.user.tipos_dispositivos_beqt.tipos.filter(Q(usa_triage=True))
        return form


class SolicitudMovimientoUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para crear `CambioDispositivo` a partir de una `SolicitudMovimiento`"""
    model = beqt_m.SolicitudMovimientoBeqt
    form_class = beqt_f.SolicitudMovimientoUpdateForm
    template_name = 'beqt/dispositivo/solicitudmovimiento_update.html'
    group_required = []

    def get_form(self, form_class=None):
        form = super(SolicitudMovimientoUpdateView, self).get_form(form_class)
        estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        if self.object.no_salida:
            dispositivos_salida = beqt_m.CambioEtapaBeqt.objects.filter(
                solicitud__no_salida = self.object.no_salida
                
            ).values('dispositivo')        

        form.fields['dispositivos'].widget = forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('beqt_api:api_dispositivo-list'),
            'data-etapa-inicial': self.object.etapa_inicial.id,
            'data-estado-inicial': estado.id,
            'data-tipo-dispositivo': self.object.tipo_dispositivo.id,
            'data-slug': self.object.tipo_dispositivo.slug,
        })

        queryset = beqt_m.DispositivoBeqt.objects.filter(
                etapa=self.object.etapa_inicial,
                tipo=self.object.tipo_dispositivo
            )

        if self.object.devolucion:
            form.fields['dispositivos'].queryset = queryset.filter(id__in=dispositivos_salida)
        else:
            form.fields['dispositivos'].queryset = queryset

        return form

    def form_valid(self, form):
        form.instance.autorizada_por = self.request.user
        form.instance.creada_por = self.request.user
        form.instance.cambiar_etapa(
            lista_dispositivos=form.cleaned_data['dispositivos'],
            usuario=self.request.user
        )
        return super(SolicitudMovimientoUpdateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
            context = super(SolicitudMovimientoUpdateView, self).get_context_data(*args, **kwargs)
            context['dispositivos_no'] = inv_m.CambioEtapa.objects.filter(solicitud=self.object.id).count()
            return context


class SolicitudMovimientoDetailView(LoginRequiredMixin, DetailView):
    """ Vista para ver los detalles de la :class:`SolicitudMovimiento`
    """
    model = beqt_m.SolicitudMovimientoBeqt
    template_name = 'beqt/dispositivo/solicitudmovimiento_detail.html'
    group_required = []


class SolicitudMovimientoListView(LoginRequiredMixin, FormView):
    """ Vista para ver la lista  de la :class:`SolicitudMovimiento`
    """
    model = beqt_m.SolicitudMovimientoBeqt
    template_name = 'beqt/dispositivo/solicitudmovimiento_list.html'
    form_class = beqt_f.SolicitudMovimientoInformeForm
    group_required = []

    def get_form(self, form_class=None):
        form = super(SolicitudMovimientoListView, self).get_form(form_class)
        form.fields['tipo_dispositivo'].queryset = self.request.user.tipos_dispositivos_beqt.tipos.all()
        return form

    """def get_context_data(self, **kwargs):
        context = super(SolicitudMovimientoListView, self).get_context_data(**kwargs)
        tipo_dis = self.request.user.tipos_dispositivos.tipos.all()
        solicitudes_list = inv_m.SolicitudMovimiento.objects.filter(tipo_dispositivo__in=tipo_dis)

        context['solicitudmovimiento_list'] = solicitudes_list
        return context"""


######################################
# VISTAS ESPECÍFICAS DE DISPOSITIVOS #
######################################

class LaptopDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`Laptop`"""
    model = beqt_m.LaptopBeqt
    template_name = 'beqt/dispositivo/laptop/laptop_detail.html'


class LaptopUptadeView(LoginRequiredMixin, UpdateView):
    """ Esta clase sirve para actualizar la  :class:`Laptop`
     mostrando los datos necesarios
    """
    model = beqt_m.LaptopBeqt
    form_class = beqt_f.LaptopForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'beqt/dispositivo/laptop/laptop_edit.html'

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        hdd = form.cleaned_data['disco_duro']
        if hdd:
            disco = beqt_m.HDDBeqt.objects.get(triage=hdd)
            disco.asignado = True
            disco.creada_por = self.request.user
            disco.save()

        return super(LaptopUptadeView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context =super(LaptopUptadeView,self).get_context_data(**kwargs)
        try:
            context["disco_duro"]=self.object.disco_duro.id
            disco = beqt_m.HDDBeqt.objects.get(id=self.object.disco_duro.id)
            context["triage"]=self.object.disco_duro
        except:
            context["disco_duro"]="---------"
            context["triage"]="-----------"
        return context

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('laptop_detail', kwargs={'triage': self.object.triage})


class TabletDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`Tablet`"""
    model = beqt_m.TabletBeqt
    template_name = 'beqt/dispositivo/tablet/tablet_detail.html'


class TabletUptadeView(LoginRequiredMixin, UpdateView):
    """ Esta clase sirve para actualizar la  :class:`Tablet`
     mostrando los datos necesarios
    """
    model = beqt_m.TabletBeqt
    form_class = beqt_f.TabletForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'beqt/dispositivo/tablet/tablet_edit.html'

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        return super(TabletUptadeView, self).form_valid(form)

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('tablet_detail', kwargs={'triage': self.object.triage})


class HDDDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`HDD`"""
    model = beqt_m.HDDBeqt
    template_name = 'beqt/dispositivo/hdd/hdd_detail.html'


class HDDUptadeView(LoginRequiredMixin, UpdateView):
    """ Esta clase sirve para actualizar la  :class:`HDD`
     mostrando los datos necesarios
    """
    model = beqt_m.HDDBeqt
    form_class = beqt_f.HDDForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'beqt/dispositivo/hdd/hdd_edit.html'

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        return super(HDDUptadeView, self).form_valid(form)

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('hdd_detail', kwargs={'triage': self.object.triage})




class DispositivoAccessPointDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Vista de detalle de dispositivos tipo :class:`DispositivoRed`"""
    model = beqt_m.AccessPointBeqt
    template_name = 'beqt/dispositivo/ap/ap_detail.html'


class DispositivoAccessPointUptadeView(LoginRequiredMixin, UpdateView):
    """ Vista actualizar los  dispositivos tipo :class:`DispositivoRed`
    """
    model = beqt_m.AccessPointBeqt
    form_class = beqt_f.DispositivoAccessPointForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'beqt/dispositivo/ap/ap_edit.html'

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        return super(DispositivoAccessPointUptadeView, self).form_valid(form)

    def get_success_url(self):
        if self.object.entrada_detalle.id != 1:
            return reverse_lazy('detalles_dispositivos', kwargs={'pk': self.object.entrada, 'detalle': self.object.entrada_detalle.id})
        else:
            return reverse_lazy('ap_detail', kwargs={'triage': self.object.triage})


class DispositivoTipoCreateView(LoginRequiredMixin, CreateView):
    """Creacion de tipos por medio la :class:`DispositivoTipo`
    """

    model = beqt_m.DispositivoTipoBeqt
    template_name = 'beqt/dispositivo/dispositivotipo_add.html'
    form_class = beqt_f.DispositivoTipoForm

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        return super(DispositivoTipoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DispositivoTipoCreateView, self).get_context_data(**kwargs)
        context['dispositivotipo_list'] = beqt_m.DispositivoTipoBeqt.objects.all()
        return context

    def get_success_url(self):
        return reverse('dispositivo_list')


class DispositivoQRprint(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """ Vista encargada de imprimir los codigos qr de  la class `Dispositivo`
    """
    model = beqt_m.DispositivoBeqt
    template_name = 'beqt/dispositivo/dispositivo_print.html'
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    group_required = []


class DispositivosTarimaListView(LoginRequiredMixin, FormView):
    """ Vista Encargada de crear los informes de  las Dispositivo obteniendo los datos
    desde el DRF
    """
    model = beqt_m.DispositivoBeqt
    template_name = 'beqt/dispositivo/dispositivo_tarima_list.html'
    form_class = beqt_f.DispositivosTarimaFormNew


class DispositivosTarimaQr(LoginRequiredMixin, DetailView):
    """Vista encargada de imprimir la lista de codigos qr generada por `DispositivosTarimaListView`
    """
    model = inv_m.Tarima
    template_name = 'beqt/entrada/imprimir_qr.html'

    def get_context_data(self, **kwargs):
        tarima = self.request.GET['tarima']
        tipo = self.request.GET['tipo']
        tarima_print = beqt_m.DispositivoBeqt.objects.filter(
            tarima=tarima,
            tipo=tipo,
            estado=inv_m.DispositivoEstado.PD,
            etapa=inv_m.DispositivoEtapa.AB).order_by('triage')

        context = super(DispositivosTarimaQr, self).get_context_data(**kwargs)
        context['dispositivo_qr'] = tarima_print

        return context