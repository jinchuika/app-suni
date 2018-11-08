from django.shortcuts import reverse, render
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView, View
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, JsonRequestResponseMixin, CsrfExemptMixin
)
from apps.escuela import models as escuela_m
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f
from django import forms


class PrestamoCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Salida mediante una :class:`Prestamo`
    Funciona  para recibir los datos de un  'PrestamoForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.Prestamo
    form_class = inv_f.PrestamoForm
    template_name = 'inventario/prestamo/prestamo_add.html'

    def get_success_url(self):
        return reverse_lazy('prestamo_list')

    def form_valid(self, form):
        tipo_prestamo = form.cleaned_data['tipo_prestamo']
        print(form.cleaned_data['dispositivo'])
        if(str(tipo_prestamo) == "Prestamo"):
            fecha_estimada = datetime.now() + timedelta(days=15)
            form.instance.fecha_estimada = fecha_estimada
        form.instance.fecha_inicio = timezone.now()
        form.instance.creado_por = self.request.user
        estado_entregado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.EN)
        etapa_entregado = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
        dispositivos = inv_m.Dispositivo.objects.filter(triage=form.cleaned_data['dispositivo'])
        for asignacion in dispositivos:
            asignacion.etapa = etapa_entregado
            asignacion.estado = estado_entregado
            asignacion.save()
        return super(PrestamoCreateView, self).form_valid(form)


class PrestamoInformeView(LoginRequiredMixin, FormView):
    """Vista Encargada de crear los informes de  prestamos obteniendo los datos
    desde el DRF
    """
    model = inv_m.Prestamo
    template_name = 'inventario/prestamo/prestamo_list.html'
    form_class = inv_f.PrestamoInformeForm


class PrestamoDetailView(LoginRequiredMixin, DetailView):
    """Vista encargada de mostrar los detalles de la :class:`SalidaInventario`
    """
    model = inv_m.Prestamo
    template_name = 'inventario/prestamo/prestamo_detail.html'
