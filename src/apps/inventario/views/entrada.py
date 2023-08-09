from django.shortcuts import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView,  UpdateView, DetailView, FormView
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from braces.views import (
    LoginRequiredMixin, GroupRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f
import calendar
from datetime import datetime

class EntradaCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """Vista   para obtener los datos de Entrada mediante una :class:`entrada`
    Funciona  para recibir los datos de un  'EntradaForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """

    model = inv_m.Entrada
    form_class = inv_f.EntradaForm
    template_name = 'inventario/entrada/entrada_add.html'
    group_required = [u"inv_bodega", u"inv_admin"]

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        form.instance.recibida_por = self.request.user
        return super(EntradaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EntradaCreateView, self).get_context_data(**kwargs)
        context['listado'] = inv_m.Entrada.objects.filter(en_creacion='True')
        return context


class EntradaDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Para generar detalles de la :class:`entrada`   con sus respectivos campos.
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/entrada_detail.html'
    group_required = [u"inv_bodega", u"inv_tecnico", u"inv_admin", u"inv_cc", u"inv_conta"]


class EntradaListView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    """Vista Encargada para mostrar las Lista de la :class:'Entrada' con su respectivo
    formulario de busqueda de filtros
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/entrada_list.html'
    form_class = inv_f.EntradaInformeForm
    group_required = [u"inv_bodega", u"inv_tecnico", u"inv_admin", u"inv_cc", u"inv_conta"]


class EntradaUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """Vista para actualizar de :class:`Entrada`. con sus respectivos campos
    """
    model = inv_m.Entrada
    form_class = inv_f.EntradaUpdateForm
    template_name = 'inventario/entrada/entrada_edit.html'
    group_required = [u"inv_bodega", u"inv_tecnico", u"inv_admin", u"inv_cc"]

    def get_success_url(self):
        if self.object.en_creacion:
            return reverse('entrada_update', kwargs={'pk': self.object.id})
        else:
            return reverse('entrada_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(EntradaUpdateView, self).get_context_data(**kwargs)       
        context['EntradaDetalleForm'] = inv_f.EntradaDetalleForm(initial={'entrada': self.object})
        return context


class EntradaDetalleView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """Vista   para obtener los datos de los Detalles de Entrada mediante una :class:`EntradaDetalle`
    Funciona  para recibir los datos de un  'EntradaDetalleForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.EntradaDetalle
    form_class = inv_f.EntradaDetalleForm
    template_name = 'inventario/entrada/entradadetalle_add.html'
    group_required = [u"inv_bodega", u"inv_admin"]


class EntradaDetalleUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """Vista Encargada de actualizar los datos mediante la :class:`EntradaDetalle`.
    """
    model = inv_m.EntradaDetalle
    form_class = inv_f.EntradaDetalleUpdateForm
    template_name = 'inventario/entrada/entradadetalle_detail.html'
    group_required = [u"inv_tecnico", u"inv_admin", u"inv_cc"]

    def get_context_data(self, **kwargs):
        context = super(EntradaDetalleUpdateView, self).get_context_data(**kwargs)
        context['datos'] = inv_m.EntradaDetalle.objects.get(id=self.object.id)
        return context

    def get_initial(self):
        initial = super(EntradaDetalleUpdateView, self).get_initial()
        initial['creado_por'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse('entrada_update', kwargs={'pk': self.object.entrada.id})


class CartaAgradecimiento(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Muestra la carta agradecimiento
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/carta_agradecimiento.html'
    group_required = [u"inv_bodega", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(CartaAgradecimiento, self).get_context_data(**kwargs)
        context['dispositivotipo_list'] = inv_m.EntradaDetalle.objects.filter(entrada=self.object.id).values('descripcion').annotate(total = Sum('total'))      
        return context


class ConstanciaEntrada(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Muestra la carta agradecimiento
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/constancia_entrada.html'
    group_required = [u"inv_bodega", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(ConstanciaEntrada, self).get_context_data(**kwargs)
        context['dispositivotipo_list'] = inv_m.EntradaDetalle.objects.filter(entrada=self.object.id)
        return context


class ConstanciaUtil(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Muestra informe de la entrada en sucio
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/informe_sucio.html'
    group_required = [u"inv_bodega", u"inv_admin"]

    def get_context_data(self, **kwargs):
        lista = []
        contador = 0
        context = super(ConstanciaUtil, self).get_context_data(**kwargs)
        tipos_conta = inv_m.DispositivoTipo.objects.filter(conta=True)

        for tipo in tipos_conta:
            detalles_mes = inv_m.EntradaDetalle.objects.filter(entrada=self.object.id, tipo_dispositivo=tipo).exclude(fecha_dispositivo__isnull=True).annotate(month=ExtractMonth('fecha_dispositivo')).values('month').annotate(util=Sum('util')).annotate(total=Sum('total')).values('month','total','util')
            for mes in detalles_mes:
                responsables = []
                detalles_entrada = inv_m.EntradaDetalle.objects.filter(entrada=self.object.id, tipo_dispositivo=tipo, fecha_dispositivo__month=mes['month'])
                contador += 1
                for datos in detalles_entrada:
                    if datos.creado_por.get_full_name() not in responsables:
                        responsables.append(datos.creado_por.get_full_name())

                index = contador % 2
                diccionario = {
                    'tipo_dispositivo': tipo.tipo,
                    'cantidad': mes['total'],
                    'util': mes['util'],
                    'mes': calendar.month_name[mes['month']],
                    'index': index,
                    'creado_por': ', '.join(str(x) for x in responsables),
                }
                lista.append(diccionario)

        context['dispositivo_tipo'] = lista
        
        return context


class ImprimirQr(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """ Muestra la impresion de los Qr de los Dispositivos
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/imprimir_qr.html'
    group_required = [u"inv_bodega", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(ImprimirQr, self).get_context_data(**kwargs)
        imprimir_qr = inv_m.Dispositivo.objects.filter(entrada=self.object.id,
                                                       entrada_detalle=self.kwargs['detalle']).order_by('triage')
        for dispositivo in imprimir_qr:
            dispositivo.impreso = True
            dispositivo.save()
        context['dispositivo_qr'] = imprimir_qr        
        nueva_bitacora = inv_m.SolicitudBitacora(
            fecha_movimiento=datetime.now(),
            accion=inv_m.AccionBitacora.objects.get(id=6),
            usuario=self.request.user,
            observaciones= "Entrada No: "+str(self.object.id)+", Detalle de Entrada No:"+str(self.kwargs['detalle'])
            )
        nueva_bitacora.save()
        return context


class ReporteRepuestosQr(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Muestra los Qr de los Repuestos creados
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/imprimir_qr.html'
    group_required = [u"inv_bodega", u"inv_tecnico", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(ReporteRepuestosQr, self).get_context_data(**kwargs)
        imprimir_qr = inv_m.Repuesto.objects.filter(entrada=self.object.id,
                                                    entrada_detalle=self.kwargs['detalle']).order_by('id')
        context['dispositivo_qr'] = imprimir_qr
        return context


class EntradaDetalleDispositivos(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """ Muestra los QR por Detalle de Entrada Creados
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/dispositivos_grid.html'
    group_required = [u"inv_bodega", u"inv_tecnico", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(EntradaDetalleDispositivos, self).get_context_data(**kwargs)
        context['dispositivo_qr'] = inv_m.Dispositivo.objects.filter(entrada=self.object.id,
                                                                     entrada_detalle=self.kwargs['detalle']).order_by('triage')
        return context


class EntradaDetalleRepuesto(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """ Muestra los QR de Repuestos creados por los  `EntradaDetalle`
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/entradadetalle_repuesto.html'
    group_required = [u"inv_bodega", u"inv_tecnico", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(EntradaDetalleRepuesto, self).get_context_data(**kwargs)
        context['repuesto_qr'] = inv_m.Repuesto.objects.filter(entrada=self.object.id,
                                                               entrada_detalle=self.kwargs['detalle']).order_by('id')
        return context


class EntradaDescuentoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """Vista encargada de crear los descuentos mediante la :class:`DescuentoEntrada`
    """
    model = inv_m.DescuentoEntrada
    template_name = 'inventario/entrada/descuento_add.html'
    group_required = [u"inv_bodega", u"inv_tecnico", u"inv_admin"]


class EntradaDescuentoDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Detalles de los registros de la :class:`DescuentoEntrada`
    """
    model = inv_m.DescuentoEntrada
    template_name = 'inventario/entrada/descuento_detail.html'
    group_required = [u"inv_bodega", u"inv_tecnico", u"inv_admin"]


class EntradaDescuentoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """Vista encargada de actualizar los descuentos mediante la :class:`DescuentoEntrada`
    """
    model = inv_m.DescuentoEntrada
    template_name = 'inventario/entrada/descuento_update.html'
    group_required = [u"inv_bodega", u"inv_tecnico", u"inv_admin"]
