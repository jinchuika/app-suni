from apps.kardex.models import *
from apps.kardex.forms import *
from apps.kardex.forms import (
    EquipoForm, EntradaForm, ProveedorForm, SalidaForm,
    SalidaDetalleForm, SalidaCerrarForm, EntradaDetalleForm)
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse

import json
from datetime import date


class EquipoListView(LoginRequiredMixin, ListView):
    template_name = 'kardex/equipo_list.html'
    model = Equipo

    def get_context_data(self, **kwargs):
        context = super(EquipoListView, self).get_context_data(**kwargs)
        context['equipo_form'] = EquipoForm()
        return context


class ProveedorListView(LoginRequiredMixin, ListView):
    template_name = 'kardex/proveedor_list.html'
    model = Proveedor

    def get_context_data(self, **kwargs):
        context = super(ProveedorListView, self).get_context_data(**kwargs)
        context['proveedor_form'] = ProveedorForm()
        return context


class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'kardex/proveedor_form.html'


class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'kardex/proveedor_form.html'


class ProveedorDetailView(LoginRequiredMixin, DetailView):
    model = Proveedor
    template_name = 'kardex/proveedor_detail.html'


class EquipoCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear un :model:`kardex.Equipo`.
    Esta vista no tiene acceso mediante GET.
    """

    model = Equipo
    form_class = EquipoForm


class EntradaCreateView(LoginRequiredMixin, CreateView):
    model = Entrada
    form_class = EntradaForm
    template_name = 'kardex/entrada.html'


class EntradaDetailView(LoginRequiredMixin, DetailView):
    model = Entrada
    template_name = 'kardex/entrada_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntradaDetailView, self).get_context_data(**kwargs)
        if not self.object.terminada:
            context['detalle_form'] = EntradaDetalleForm(initial={'entrada': self.object})
            context['cerrar_form'] = EntradaCerrarForm(instance=self.object, initial={'terminada': True})
        return context


class EntradaDetalleCreateView(LoginRequiredMixin, CreateView):
    model = EntradaDetalle
    form_class = EntradaDetalleForm
    template_name = 'kardex/entrada.html'


class EntradaUpdateView(LoginRequiredMixin, UpdateView):
    model = Entrada
    form_class = EntradaCerrarForm


class SalidaListView(LoginRequiredMixin, ListView):
    model = Salida
    template_name = 'kardex/salida_list.html'

    def get_context_data(self, **kwargs):
        context = super(SalidaListView, self).get_context_data(**kwargs)
        context['salida_form'] = SalidaForm()
        return context


class SalidaCreateView(LoginRequiredMixin, CreateView):
    model = Salida
    template_name = 'kardex/salida.html'
    form_class = SalidaForm


class SalidaUpdateView(LoginRequiredMixin, UpdateView):
    model = Salida
    form_class = SalidaCerrarForm


class SalidaDetailView(LoginRequiredMixin, DetailView):
    model = Salida
    template_name = 'kardex/salida_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SalidaDetailView, self).get_context_data(**kwargs)
        if not self.object.terminada:
            context['detalle_form'] = SalidaDetalleForm(initial={'salida': self.object})
            context['cerrar_form'] = SalidaCerrarForm(instance=self.object, initial={'terminada': True})
        return context


class SalidaPrintView(LoginRequiredMixin, DetailView):
    model = Salida
    template_name = 'kardex/salida_print.html'


class SalidaDetalleCreateView(LoginRequiredMixin, CreateView):
    model = SalidaDetalle
    form_class = SalidaDetalleForm

# Desde aquí empieza el código a renovar
# 
# 
# 
# 
# 
# 
class Equipolog(LoginRequiredMixin, CreateView):
    model = Equipo
    form_class = FormularioEquipo
    template_name = "kardex/equipo.html"
    success_url = reverse_lazy('kardex_equipo')

    def get_context_data(self, **kwargs):
        context = super(Equipolog, self).get_context_data(**kwargs)
        context['lista'] = self.model.objects.all()
        return context


def informe_general(request, ini, out):
    if ini == "all":
        ini = "2000-01-01"
    if out == "all":
        out = date.today()
    equipo_list = Equipo.objects.all()
    lista_vacia = []
    for equipo in equipo_list:
        if equipo.get_cant_entradas(ini, out) != 0:
            lista_vacia.append({
                'nombre': str(equipo), 'cantidad_ingresos': equipo.get_cant_entradas(ini, out),
                'cantidad_egresos': equipo.get_cant_salidas(ini, out), 'ingreso': equipo.get_entradas(ini, out),
                'egreso': equipo.get_salidas(ini, out), 'diferencia': equipo.get_entradas(ini, out) - equipo.get_salidas(ini, out),
                'existencia_actual': equipo.get_existencia()})
    return HttpResponse(json.dumps({'properties': lista_vacia}))


class EquipoEntrada(LoginRequiredMixin, DetailView):
    model = Equipo
    def get(self, request, **kwargs):
        lista_entrada = Entrada.objects.filter(equipo = self.get_object())
        lista_vacia = []
        for ingreso in lista_entrada:
            lista_vacia.append({'id':ingreso.id, 'fecha':str(ingreso.fecha), 'cantidad': ingreso.cantidad, 'observacion':ingreso.observacion})
        return HttpResponse(
                json.dumps({
                    "tablainf": lista_vacia,
                    })
                )

class EquipoSalida(LoginRequiredMixin, DetailView):
    model = Equipo
    def get(self, request, **kwargs):
        lista_salida = Salida.objects.filter()

        lista2 = Salida.objects.filter(equipo = self.get_object())
        lista_vacia = []
        for egreso in lista2:
            lista_vacia.append({'id':egreso.id, 'tecnico':str(egreso.salida.tecnico), 'fecha': str(egreso.salida.fecha), 'cantidad': egreso.cantidad})
        return HttpResponse(
            json.dumps({
                "tablainf" : lista_vacia,
                })
            )
    


#entrada del equipo
class EntradaCreate(LoginRequiredMixin, CreateView):
    model = Entrada
    form_class = FormularioEntrada
    template_name = "kardex/entrada.html"
    success_url = reverse_lazy('kardex_equipo')
    
    def get_context_data(self, **kwargs):
        context = super(EntradaCreate, self).get_context_data(**kwargs)
        context['formulario'] = FormularioEntradaInforme
        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        precio = self.object.precio
        if precio is not None and precio <= 0:
            return self.form_invalid(form)
        else:
            self.object.save()
            return super(EntradaCreate, self).form_valid(form)

def get_informe_entradas(request, proveedor, tipo, ini, out):
    #este se quedó
    if ini == "all":
        inicio = "2000-01-01"
    else:
        inicio = ini
    
    if out == "all":
        fin = date.today()  
    else:
        fin = out   

    if tipo == "all" and proveedor == "all" :
        lista_entrada = Entrada.objects.filter(fecha__range=(inicio, fin))
    else:
        if tipo == "all":
            if proveedor != "all":
                lista_entrada = Entrada.objects.filter(fecha__range=(inicio, fin), proveedor__id = proveedor)
        else:
            if proveedor != "all":
                lista_entrada = Entrada.objects.filter(fecha__range=(inicio, fin), proveedor__id=proveedor, tipo_entrada__id=tipo)
            else:
                lista_entrada = Entrada.objects.filter(fecha__range=(inicio, fin), tipo_entrada__id=tipo)

    lista_vacia = []
    if tipo == "2":
        for ingreso in lista_entrada:
            lista_vacia.append({'id':ingreso.id, 'equipo':str(ingreso.equipo), 'tipo':str(ingreso.tipo_entrada), 'prov': str(ingreso.proveedor), 'fecha':str(ingreso.fecha), 'cantidad': ingreso.cantidad, 'precio':str(ingreso.precio), 'factura':str(ingreso.factura)})
    else:
        for ingreso in lista_entrada:
            lista_vacia.append({'id':ingreso.id, 'equipo':str(ingreso.equipo), 'tipo':str(ingreso.tipo_entrada), 'prov': str(ingreso.proveedor), 'fecha':str(ingreso.fecha), 'cantidad': ingreso.cantidad})

    return HttpResponse(
            json.dumps({
                "tablainf": lista_vacia,
                })
            )

#Salida del equipo
class SalidaCreate(LoginRequiredMixin, CreateView):
    model = Salida
    form_class = FormularioSalida
    template_name = "kardex/salida.html"
    success_url = reverse_lazy('kardex_equipo')
    def get_context_data(self, **kwargs):
        context = super(SalidaCreate, self).get_context_data(**kwargs)
        context['formulario'] = FormularioSalidaInforme
        return context

def get_informe_salidas(request, tecnico, ini, out):
    if ini == "all":
        inicio = "2000-01-01"
    else:
        inicio = ini
    if out == "all":
        fin = date.today()
    else:
        fin = out

    if tecnico == "all":
        lista_entrada = Salida.objects.filter( salida__fecha__range=(inicio, fin))
    else:
        lista_entrada = Salida.objects.filter(salida__tecnico__id=tecnico, salida__fecha__range=(inicio, fin))
    
    lista_vacia = []
    for salida in lista_entrada:
        lista_vacia.append({'id':salida.id, 'tecnico':str(salida.salida.tecnico), 'fecha': str(salida.salida.fecha), 'equipo':str(salida.equipo), 'cantidad': salida.cantidad})
    
    return HttpResponse(
            json.dumps({
                "tablainf": lista_vacia, 
                })
            )

    


class ProveedorCreate(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = FormularioProveedor
    template_name = "kardex/proveedor.html"
    success_url = reverse_lazy('kardex_proveedor')
    def get_context_data(self, **kwargs):
        context = super(ProveedorCreate, self).get_context_data(**kwargs)
        context['lista'] = Proveedor.objects.all()
        return context
