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

    def get_form(self, form_class=None):
        form = super(RepuestosAsignacionCreateView, self).get_form(form_class)
        form.fields['tipo'].queryset = self.request.user.tipos_dispositivos.tipos.all().filter(usa_triage=True)
        return form


class RepuestosDetailView(LoginRequiredMixin, DetailView):
    """Generar detalles de la :class:`Repuesto`   con sus respectivos campos.
    """
    model = inv_m.Repuesto
    template_name = 'inventario/repuesto/repuesto_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RepuestosDetailView, self).get_context_data(**kwargs)
        comentarios=inv_m.RepuestoComentario.objects.filter(repuesto=self.object.id)   
        context['comentarios'] = comentarios
        return context


class RepuestosUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizacion  de la :class:`entrada`   con sus respectivos campos..
    """
    model = inv_m.Repuesto
    template_name = 'inventario/repuesto/repuesto_edit.html'
    form_class = inv_f.RepuestosUpdateForm

    def get_success_url(self):
        return reverse_lazy('repuesto_detail', kwargs={'pk': self.object.id})


class RepuestosQRprint(LoginRequiredMixin, DetailView):
    """Vista encargada de imprimir los Qr de la :class:`Repuesto`
    """
    model = inv_m.Repuesto
    template_name = 'inventario/repuesto/repuesto_print.html'


class RepuestosQRprintList(LoginRequiredMixin, DetailView):
    """Vista encargada de imprimir los Qr de la :class:`Repuesto`
    """
    model = inv_m.Repuesto
    template_name = 'inventario/repuesto/imprimir_qr_list.html'

    def get_context_data(self, **kwargs):
        print(self.request)
        no = self.request.GET['id']
        tarima = self.request.GET['tarima']
        tipo = self.request.GET['tipo']
        marca = self.request.GET['marca']
        modelo = self.request.GET['modelo']

        tarima_print = inv_m.Repuesto.objects.all()
        if no:
            tarima_print = inv_m.Repuesto.objects.filter(id=no)
        else: 
            if tarima:
                tarima_print = tarima_print.filter(tarima=tarima).order_by('id')
            if tipo:
                tarima_print = tarima_print.filter(tipo=tipo).order_by('id')
            if marca:
                tarima_print = tarima_print.filter(marca=marca).order_by('id')
            if modelo:
                tarima_print = tarima_print.filter(modelo=modelo).order_by('id')

        context = super(RepuestosQRprintList, self).get_context_data(**kwargs)
        context['dispositivo_qr'] = tarima_print
        return context
