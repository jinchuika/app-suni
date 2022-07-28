from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView,  UpdateView, DetailView, FormView, TemplateView
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from braces.views import (
    LoginRequiredMixin, GroupRequiredMixin
)
from apps.recaudacionFondos import models as rf_m
from apps.recaudacionFondos import forms as rf_f
import calendar
from django.urls import reverse_lazy

# Create your views here.
class ProveedorUptadeView(LoginRequiredMixin, UpdateView):
    """Actualizacion  de la :class:`Proveedores`   con sus respectivos campos..
    """
    model = rf_m.Proveedor
    form_class = rf_f.ProveedoresUpdateForm
    template_name = 'recaudacionFondos/proveedores_edit.html'


class ProveedorDetailView(LoginRequiredMixin, TemplateView):
    """Actualizacion  de la :class:`Proveedores`   con sus respectivos campos..
    """
    template_name = 'recaudacionFondos/proveedores_detail.html'

class EntradaCreateView(LoginRequiredMixin, CreateView):
    #group_required = [u"kardex", ]
    model = rf_m.Entrada
    form_class = rf_f.EntradaForm
    template_name = 'recaudacionFondos/entrada_add.html'
    def get_context_data(self, **kwargs):
        context = super(EntradaCreateView, self).get_context_data(**kwargs)
        context['pendientes_list'] = rf_m.Entrada.objects.filter(terminada=False)
        context['filter_form'] = rf_f.RecaudacionInformeForm()
        return context


class EntradaDetailView(LoginRequiredMixin, DetailView):
    #group_required = [u"kardex", ]
    model = rf_m.Entrada
    template_name = 'recaudacionFondos/entrada_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntradaDetailView, self).get_context_data(**kwargs)
        if not self.object.terminada:
            context['detalle_form'] = rf_f.EntradaDetalleForm(initial={'entrada': self.object})
            #context['cerrar_form'] = EntradaCerrarForm(instance=self.object, initial={'terminada': True})
        return context

class EntradaDetalleCreateView(LoginRequiredMixin, CreateView):
    #group_required = [u"kardex", ]
    model = rf_m.DetalleEntrada
    form_class = rf_f.EntradaDetalleForm
    template_name = 'recaudacionFondos/entrada_add.html'


class ArticuloCreateView(LoginRequiredMixin, CreateView):
    #group_required = [u"kardex", ]
    model = rf_m.Articulo
    form_class = rf_f.ArticuloForm
    template_name = 'recaudacionFondos/articulo_add.html'

    def get_success_url(self):
        return reverse_lazy('recaudacion_articulo_add')


class SalidaCreateView(LoginRequiredMixin, CreateView):
    #group_required = [u"kardex", ]
    model = rf_m.Salida
    form_class = rf_f.SalidaForm
    template_name = 'recaudacionFondos/salida_add.html'
    def get_context_data(self, **kwargs):
        context = super(SalidaCreateView, self).get_context_data(**kwargs)
        context['pendientes_list'] = rf_m.Salida.objects.filter(terminada=False)
        context['filter_form'] = rf_f.RecaudacionInformeForm()
        return context
    def get_success_url(self):
        return reverse_lazy('recaudacion_salida_update', kwargs={'pk': self.object.id})

class SalidaUpdateView(LoginRequiredMixin, UpdateView):
    #group_required = [u"kardex", ]
    model = rf_m.Salida
    form_class = rf_f.SalidaForm
    template_name = 'recaudacionFondos/salida_edit.html'
    def get_success_url(self):
        return reverse_lazy('recaudacion_salida_update', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(SalidaUpdateView, self).get_context_data(**kwargs)
        if not self.object.terminada:
            context['detalle_form'] = rf_f.SalidaDetalleForm(initial={'salida': self.object})
            #context['cerrar_form'] = EntradaCerrarForm(instance=self.object, initial={'terminada': True})
        return context


class SalidaDetailView(LoginRequiredMixin, DetailView):
    #group_required = [u"kardex", ]
    model = rf_m.Salida
    template_name = 'recaudacionFondos/salida_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SalidaDetailView, self).get_context_data(**kwargs)
        if not self.object.terminada:
            context['detalle_form'] = rf_f.SalidaDetalleForm(initial={'salida': self.object})
            #context['cerrar_form'] = EntradaCerrarForm(instance=self.object, initial={'terminada': True})
        return context

class SalidaDetalleCreateView(LoginRequiredMixin, CreateView):
    #group_required = [u"kardex", ]
    model = rf_m.DetalleSalida
    form_class = rf_f.SalidaDetalleForm
    template_name = 'recaudacionFondos/salida_add.html'
