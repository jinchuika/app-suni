from django.shortcuts import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView,  UpdateView, DetailView, FormView
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from braces.views import (
    LoginRequiredMixin, GroupRequiredMixin
)
from apps.beqt import models as beqt_m
from apps.beqt import forms as beqt_f
import calendar


class EntradaCreateView(LoginRequiredMixin, CreateView,GroupRequiredMixin):
    """Vista   para obtener los datos de Entrada mediante una :class:`entrada`
    Funciona  para recibir los datos de un  'EntradaForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET. para el modulo de beqt
    """

    model = beqt_m.Entrada
    form_class = beqt_f.EntradaForm
    template_name = 'beqt/entrada/entrada_add.html'
    group_required = [u"beqt_bodega", u"inv_admin"]  

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        form.instance.recibida_por = self.request.user
        return super(EntradaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EntradaCreateView, self).get_context_data(**kwargs)
        context['listado'] = beqt_m.Entrada.objects.filter(en_creacion='True')
        return context

class EntradaDetailView(LoginRequiredMixin,  DetailView,GroupRequiredMixin):
    """Para generar detalles de la :class:`entrada`   con sus respectivos campos.
    """
    model = beqt_m.Entrada
    template_name = 'beqt/entrada/entrada_detail.html'
    group_required = [u"beqt_bodega", u"beqt_tecnico", u"inv_admin", u"beqt_cc", u"inv_conta"]


class EntradaListView(LoginRequiredMixin,  FormView,GroupRequiredMixin):
    """Vista Encargada para mostrar las Lista de la :class:'Entrada' con su respectivo
    formulario de busqueda de filtros
    """
    model = beqt_m.Entrada
    template_name = 'beqt/entrada/entrada_list.html'
    form_class = beqt_f.EntradaInformeForm
    group_required = [u"beqt_bodega", u"beqt_tecnico", u"inv_admin", u"beqt_cc", u"inv_conta"]


class EntradaUpdateView(LoginRequiredMixin, UpdateView,GroupRequiredMixin):
    """Vista para actualizar de :class:`Entrada`. con sus respectivos campos
    """
    model = beqt_m.Entrada
    form_class = beqt_f.EntradaUpdateForm
    template_name = 'beqt/entrada/entrada_edit.html'
    group_required = [u"beqt_bodega", u"beqt_tecnico", u"inv_admin", u"beqt_cc"]

    def get_success_url(self):
        if self.object.en_creacion:
            return reverse('entrada_beqt_update', kwargs={'pk': self.object.id})
        else:
            return reverse('entrada_beqt_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(EntradaUpdateView, self).get_context_data(**kwargs)
        context['EntradaDetalleForm'] = beqt_f.EntradaDetalleForm(initial={'entrada': self.object})
        return context

class EntradaDetalleView(LoginRequiredMixin, CreateView,GroupRequiredMixin):
    """Vista   para obtener los datos de los Detalles de Entrada mediante una :class:`EntradaDetalle`
    Funciona  para recibir los datos de un  'EntradaDetalleForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = beqt_m.EntradaDetalleBeqt
    form_class = beqt_f.EntradaDetalleForm
    template_name = 'beqt/entrada/entradadetalle_add.html'
    group_required = [u"beqt_bodega",u"inv_admin"]


class EntradaDetalleUpdateView(LoginRequiredMixin, UpdateView,GroupRequiredMixin):
    """Vista Encargada de actualizar los datos mediante la :class:`EntradaDetalle`.
    """
    model = beqt_m.EntradaDetalleBeqt
    form_class = beqt_f.EntradaDetalleUpdateForm
    template_name = 'beqt/entrada/entradadetalle_detail.html'
    group_required = [u"beqt_bodega", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(EntradaDetalleUpdateView, self).get_context_data(**kwargs)
        detalle = beqt_m.EntradaDetalleBeqt.objects.get(id=self.object.id)
        print(detalle.total * 1)
        context['datos'] = beqt_m.EntradaDetalleBeqt.objects.get(id=self.object.id)
        
        return context

    def get_initial(self):
        initial = super(EntradaDetalleUpdateView, self).get_initial()
        initial['creado_por'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse('entrada_beqt_update', kwargs={'pk': self.object.entrada.id})


class ImprimirQr(LoginRequiredMixin, DetailView,GroupRequiredMixin):
    """ Muestra la impresion de los Qr de los Dispositivos
    """
    model = beqt_m.Entrada
    template_name = 'beqt/entrada/imprimir_qr.html'
    group_required = [u"beqt_bodega", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(ImprimirQr, self).get_context_data(**kwargs)
        imprimir_qr = beqt_m.DispositivoBeqt.objects.filter(entrada=self.object.id,
                                                       entrada_detalle=self.kwargs['detalle']).order_by('triage')
        for dispositivo in imprimir_qr:
            dispositivo.impreso = True
            dispositivo.save()
        context['dispositivo_qr'] = imprimir_qr
        return context

class EntradaDetalleDispositivos(LoginRequiredMixin, DetailView,GroupRequiredMixin):
    """ Muestra los QR por Detalle de Entrada Creados
    """
    model = beqt_m.Entrada
    template_name = 'beqt/entrada/dispositivos_grid.html'
    group_required = [u"beqt_bodega", u"beqt_tecnico", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(EntradaDetalleDispositivos, self).get_context_data(**kwargs)
        context['dispositivo_qr'] = beqt_m.DispositivoBeqt.objects.filter(entrada=self.object.id,
                                                                     entrada_detalle=self.kwargs['detalle']).order_by('triage')
        return context


class CartaAgradecimiento(LoginRequiredMixin, DetailView,GroupRequiredMixin):
    """Muestra la carta agradecimiento
    """
    model = beqt_m.Entrada
    template_name = 'beqt/entrada/carta_agradecimiento.html'
    group_required = [u"beqt_bodega", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(CartaAgradecimiento, self).get_context_data(**kwargs)
        context['dispositivotipo_list'] = beqt_m.EntradaDetalleBeqt.objects.filter(entrada=self.object.id).values('descripcion').annotate(total = Sum('total'))      
        return context


class ConstanciaEntrada(LoginRequiredMixin, DetailView,GroupRequiredMixin):
    """Muestra la carta agradecimiento
    """
    model = beqt_m.Entrada
    template_name = 'inventario/entrada/constancia_entrada.html'
    group_required = [u"beqt_bodega", u"inv_admin"]

    def get_context_data(self, **kwargs):
        context = super(ConstanciaEntrada, self).get_context_data(**kwargs)
        context['dispositivotipo_list'] = beqt_m.EntradaDetalleBeqt.objects.filter(entrada=self.object.id)
        return context


class ConstanciaUtil(LoginRequiredMixin, DetailView,GroupRequiredMixin):
    """Muestra informe de la entrada en sucio
    """
    model = beqt_m.Entrada
    template_name = 'beqt/entrada/informe_sucio.html'
    group_required = [u"beqt_bodega", u"inv_admin"]

    def get_context_data(self, **kwargs):
        lista = []
        contador = 0
        context = super(ConstanciaUtil, self).get_context_data(**kwargs)
        #tipos_conta = beqt_m.DispositivoTipoBeqt.objects.filter(conta=True)
        tipos_conta = beqt_m.DispositivoTipoBeqt.objects.all()
        for tipo in tipos_conta:
            detalles_mes = beqt_m.EntradaDetalleBeqt.objects.filter(entrada=self.object.id, tipo_dispositivo=tipo).exclude(fecha_dispositivo__isnull=True).annotate(month=ExtractMonth('fecha_dispositivo')).values('month').annotate(total=Sum('total')).values('month','total')
            for mes in detalles_mes:
                responsables = []
                detalles_entrada = beqt_m.EntradaDetalleBeqt.objects.filter(entrada=self.object.id, tipo_dispositivo=tipo, fecha_dispositivo__month=mes['month'])
                contador += 1
                for datos in detalles_entrada:
                    if datos.creado_por.get_full_name() not in responsables:
                        responsables.append(datos.creado_por.get_full_name())

                index = contador % 2
                diccionario = {
                    'tipo_dispositivo': tipo.tipo,
                    'cantidad': mes['total'],                   
                    'mes': calendar.month_name[mes['month']],
                    'index': index,
                    'creado_por': ', '.join(str(x) for x in responsables),
                }
                lista.append(diccionario)

        context['dispositivo_tipo'] = lista
        
        return context