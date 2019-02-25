from django.shortcuts import render
from django.urls import reverse_lazy
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin,
    CsrfExemptMixin, JsonRequestResponseMixin)
from django.views.generic import DetailView, ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from apps.conta import models as conta_m
from apps.inventario import models as inv_m
from apps.conta import forms as conta_f
from rest_framework import views, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime, timedelta
from django.db.models import Sum


class PeriodoFiscalCreateView(LoginRequiredMixin, CreateView):
    """ Vista   para obtener los datos de Periodo Fiscal mediante una :class:`PeriodoFiscal`
    Funciona  para recibir los datos de un  'PeriodoFiscalForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PeriodoFiscal
    template_name = 'conta/periodo_add.html'
    form_class = conta_f.PeriodoFiscalForm

    def get_success_url(self):
        return reverse_lazy('periodo_list')


class PeriodoFiscalListView(LoginRequiredMixin, ListView):
    """ Vista para Los listados de :class:`PeriodoFiscal`. con sus respectivos datos
    """
    model = conta_m.PeriodoFiscal
    template_name = 'conta/periodo_list.html'


class PeriodoFiscalDetailView(LoginRequiredMixin, DetailView):
    """Vista para detalle de :class:`PeriodoFiscal`.
    """
    model = conta_m.PeriodoFiscal
    template_name = 'conta/periodo_detail.html'


class PeriodoFiscalUpdateView(LoginRequiredMixin, UpdateView):
    """ Vista   para obtener los datos de Periodo Fiscal mediante una :class:`PeriodoFiscal`
    Funciona  para recibir los datos de un  'PeriodoFiscalUpdateForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PeriodoFiscal
    template_name = 'conta/periodo_edit.html'
    form_class = conta_f.PeriodoFiscalUpdateForm

    def get_success_url(self):
        return reverse_lazy('periodo_list')


class PrecioEstandarCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Precio Estandar mediante una :class:`PrecioEstandar`
    Funciona  para recibir los datos de un  'PrecioEstandarForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PrecioEstandar
    template_name = 'conta/precioestandar_add.html'
    form_class = conta_f.PrecioEstandarForm

    def form_valid(self, form):
        periodo_activo = conta_m.PeriodoFiscal.objects.get(actual=True)
        form.instance.creado_por = self.request.user
        form.instance.periodo = periodo_activo
        return super(PrecioEstandarCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('precioestandar_list')


class PrecioEstandarListView(LoginRequiredMixin, FormView):
    """Vista   para obtener los datos de PrecioEstandar mediante una :class:`PrecioEstandar`
    Funciona  para recibir los datos de un  'PrecioEstandarInformeForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PrecioEstandar
    template_name = 'conta/precioestandar_list.html'
    form_class = conta_f.PrecioEstandarInformeForm


class PrecioEstandarInformeListView(LoginRequiredMixin, FormView):
    """Vista   para obtener los datos de PrecioEstandar mediante una :class:`PrecioEstandar`
    Funciona  para recibir los datos de un  'PrecioEstandarInformeForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PrecioEstandar
    template_name = 'conta/informe_existencia.html'
    form_class = conta_f.CantidadInformeForm


class PeriofoFiscalPorExistenciaInformeListView(LoginRequiredMixin, FormView):
    """Vista   para obtener los datos de PrecioEstandar mediante una :class:`PrecioEstandar`
    Funciona  para recibir los datos de un  'PrecioEstandarInformeForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PrecioEstandar
    template_name = 'conta/precioestandar_informe.html'
    form_class = conta_f.PrecioEstandarInformeForm


class ContabilidadEntradaInformeListView(LoginRequiredMixin, FormView):
    """Vista   para obtener los datos de PrecioEstandar mediante una :class:`PrecioEstandar`
    Funciona  para recibir los datos de un  'PrecioEstandarInformeForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = conta_m.PrecioEstandar
    template_name = 'conta/informe_entrada.html'
    form_class = conta_f.EntradaInformeForm


class InformeCantidadJson(views.APIView):
    def get(self, request):
        repuesto_dispositivo = self.request.GET['dispositivo']
        id_periodo = self.request.GET['periodo']
        dispositivos = inv_m.DispositivoTipo.objects.all().exclude(conta=False)
        lista_dispositivos = {}
        lista = []
        acumulador_anterior = 0
        acumulador = 0
        periodo = conta_m.PeriodoFiscal.objects.get(id=id_periodo)
        nueva_fecha = periodo.fecha_fin - timedelta(days=365)
        nueva_fecha_inicio = periodo.fecha_inicio - timedelta(days=365)
        periodo_anterior = conta_m.PeriodoFiscal.objects.get(fecha_fin=nueva_fecha)
        periodos_anteriores = conta_m.PeriodoFiscal.objects.filter(fecha_fin__lt=periodo.fecha_inicio).values('id')
        print(nueva_fecha_inicio)
        try:
            for tipo in dispositivos:
                precio_tipo_dispositivo = 0
                precio_tipo_compras = 0
                dispositivo = {}
                if repuesto_dispositivo == str(1):
                    # Obtener Listado de bajas, compras y útiles
                    bajas = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=-1,
                        dispositivo__tipo=tipo,
                        fecha__lte=nueva_fecha).values('dispositivo')
                    compras = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=1,
                        dispositivo__tipo=tipo,
                        fecha__lte=nueva_fecha,
                        dispositivo__entrada__tipo__contable=True).exclude(dispositivo__in=bajas).values('dispositivo')
                    utiles = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=1,
                        dispositivo__tipo=tipo,
                        fecha__lte=nueva_fecha).exclude(
                            dispositivo__in=bajas).exclude(dispositivo__in=compras).values('dispositivo')

                    # Obtener Total Anterior
                    if periodo_anterior.fecha_fin.year <= 2018:
                        precio_tipo_dispositivo = conta_m.PrecioDispositivo.objects.filter(
                            dispositivo__in=utiles,
                            periodo__in=periodos_anteriores).aggregate(Sum('precio'))
                    else:
                        precio_tipo_dispositivo = conta_m.PrecioDispositivo.objects.filter(
                            dispositivo__in=utiles,
                            periodo=periodo_anterior).aggregate(Sum('precio'))

                    precio_tipo_compras = conta_m.PrecioDispositivo.objects.filter(
                        dispositivo__in=compras,
                        activo=True).aggregate(Sum('precio'))

                    if precio_tipo_dispositivo['precio__sum'] is not None:
                        precio_tipo_dispositivo = precio_tipo_dispositivo['precio__sum']
                    else:
                        precio_tipo_dispositivo = 0

                    if precio_tipo_compras['precio__sum'] is not None:
                        precio_tipo_compras = precio_tipo_compras['precio__sum']
                    else:
                        precio_tipo_compras = 0

                    precio_total_anterior = precio_tipo_dispositivo + precio_tipo_compras
                    acumulador_anterior += precio_total_anterior

                    # Obtener Precio Estandar Actual y Anterior
                    precio = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo,
                        periodo=periodo,
                        inventario='dispositivo').first()

                    precio_anterior = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo,
                        periodo=periodo_anterior,
                        inventario='dispositivo').first()

                    # Obtener Total Actual
                    precio_tipo_dispositivo = conta_m.PrecioDispositivo.objects.filter(
                        dispositivo__in=utiles,
                        periodo=periodo).aggregate(Sum('precio'))
                    precio_tipo_compras = conta_m.PrecioDispositivo.objects.filter(
                        dispositivo__in=compras,
                        activo=True).aggregate(Sum('precio'))

                    if precio_tipo_dispositivo['precio__sum'] is not None:
                        precio_tipo_dispositivo = precio_tipo_dispositivo['precio__sum']
                    else:
                        if precio is not None:
                            precio_tipo_dispositivo = len(utiles) * precio.precio
                        else:
                            precio_tipo_dispositivo = 0

                    if precio_tipo_compras['precio__sum'] is not None:
                        precio_tipo_compras = precio_tipo_compras['precio__sum']
                    else:
                        precio_tipo_compras = 0

                    precio_total = precio_tipo_dispositivo + precio_tipo_compras
                    acumulador += precio_total
                else:
                    bajas = conta_m.MovimientoRepuesto.objects.filter(
                        tipo_movimiento=-1,
                        repuesto__tipo=tipo,
                        fecha__lte=nueva_fecha).values('repuesto')
                    compras = conta_m.MovimientoRepuesto.objects.filter(
                        tipo_movimiento=1,
                        repuesto__tipo=tipo,
                        fecha__lte=nueva_fecha,
                        repuesto__entrada__tipo__contable=True).exclude(repuesto__in=bajas).values('repuesto')
                    utiles = conta_m.MovimientoRepuesto.objects.filter(
                        tipo_movimiento=1,
                        repuesto__tipo=tipo,
                        fecha__lte=nueva_fecha).exclude(
                            repuesto__in=bajas).exclude(repuesto__in=compras).values('repuesto')
                    # Obtener Total Anterior
                    if periodo_anterior.fecha_fin.year <= 2018:
                        precio_tipo_dispositivo = conta_m.PrecioRepuesto.objects.filter(
                            repuesto__in=utiles,
                            periodo__in=periodos_anteriores).aggregate(Sum('precio'))
                    else:
                        precio_tipo_dispositivo = conta_m.PrecioRepuesto.objects.filter(
                            repuesto__in=utiles,
                            periodo=periodo_anterior).aggregate(Sum('precio'))

                    precio_tipo_compras = conta_m.PrecioRepuesto.objects.filter(
                        repuesto__in=compras,
                        activo=True).aggregate(Sum('precio'))

                    if precio_tipo_dispositivo['precio__sum'] is not None:
                        precio_tipo_dispositivo = precio_tipo_dispositivo['precio__sum']
                    else:
                        precio_tipo_dispositivo = 0

                    if precio_tipo_compras['precio__sum'] is not None:
                        precio_tipo_compras = precio_tipo_compras['precio__sum']
                    else:
                        precio_tipo_compras = 0
                    precio_total_anterior = precio_tipo_dispositivo + precio_tipo_compras
                    acumulador_anterior += precio_total_anterior
                    # Obtener Precio Estandar Actual y Anterior
                    precio = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo,
                        periodo=periodo,
                        inventario='repuesto').first()

                    precio_anterior = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo,
                        periodo=periodo_anterior,
                        inventario='repuesto').first()
                    # Obtener Total Actual
                    precio_tipo_dispositivo = conta_m.PrecioRepuesto.objects.filter(
                        repuesto__in=utiles,
                        periodo=periodo).aggregate(Sum('precio'))
                    precio_tipo_compras = conta_m.PrecioRepuesto.objects.filter(
                        repuesto__in=compras,
                        activo=True).aggregate(Sum('precio'))

                    if precio_tipo_dispositivo['precio__sum'] is not None:
                        precio_tipo_dispositivo = precio_tipo_dispositivo['precio__sum']
                    else:
                        if precio is not None:
                            precio_tipo_dispositivo = len(utiles) * precio.precio
                        else:
                            precio_tipo_dispositivo = 0

                    if precio_tipo_compras['precio__sum'] is not None:
                        precio_tipo_compras = precio_tipo_compras['precio__sum']
                    else:
                        precio_tipo_compras = 0

                    precio_total = precio_tipo_dispositivo + precio_tipo_compras
                    acumulador += precio_total
                disponible = len(utiles) + len(compras)
                if precio is not None and precio_anterior is not None:
                    dispositivo['tipo'] = tipo.tipo
                    dispositivo['cantidad'] = disponible
                    dispositivo['precio'] = str(precio.precio)
                    dispositivo['precio_anterior'] = precio_anterior.precio
                    dispositivo['total_anterior'] = precio_total_anterior
                    dispositivo['total'] = precio_total
                    dispositivo['acumulador_total'] = acumulador
                    dispositivo['acumulador_anterior'] = acumulador_anterior
                    lista.append(dispositivo)
                    lista_dispositivos[tipo.tipo] = dispositivo
            return Response(lista)
        except ObjectDoesNotExist as e:
            return Response(
                {
                    'mensaje': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class InformeEntradaJson(views.APIView):
    """ Si es Donacion o Contenedor ir a traer el precio estandar del modelo de contabilidad
    en caso contrario desde el precio_unitario del detalle de entrada
    """
    def get(self, request):
        try:
            donante = self.request.GET['donante']
        except MultiValueDictKeyError as e:
            donante = 0
        try:
            tipo_entrada = self.request.GET['tipo_entrada']
        except MultiValueDictKeyError as e:
            tipo_entrada = 0
        tipo_dispositivo = self.request.GET['tipo_dispositivo']
        fecha_inicio = self.request.GET['fecha_min']
        fecha_fin = self.request.GET['fecha_max']
        validar_fecha = conta_m.PeriodoFiscal.objects.filter(fecha_inicio__lte=fecha_inicio, fecha_fin__gte=fecha_fin)
        new_dispositivo = inv_m.DispositivoTipo.objects.get(id=tipo_dispositivo)
        if validar_fecha.count() == 1:
            print("Si existe en el periodo fiscal")
            lista_dispositivos = {}
            lista = []
            if(donante == 0):
                print("no hay donante")
                if(tipo_entrada == 0):
                    entrada = inv_m.EntradaDetalle.objects.filter(
                        entrada__fecha_cierre__gte=fecha_inicio,
                        entrada__fecha_cierre__lte=fecha_fin,
                        tipo_dispositivo=tipo_dispositivo,
                        ).exclude(entrada__tipo__nombre='Especial')
                    new_tipo_dispositivo = inv_m.EntradaTipo.objects.all().exclude(nombre='Especial')
                    # totale cuando no hay donante
                    altas = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__lte=fecha_inicio,
                        ).count()
                    bajas = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=-1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__lte=fecha_inicio,
                        ).count()
                    total_final = altas - bajas
                    precio = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo_dispositivo,
                        inventario='dispositivo',
                        periodo__fecha_inicio__lte=fecha_inicio,
                        periodo__fecha_fin__gte=fecha_fin).first()
                    if precio is not None:
                        total_costo = precio.precio * total_final
                    else:
                        total_costo = 1 * total_final
                    # totales finales
                    altas_despues = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__range=[fecha_inicio, fecha_fin],
                        ).count()
                    bajas_despues = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=-1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__range=[fecha_inicio, fecha_fin],
                        ).count()
                    total_despues = altas_despues - bajas_despues
                    precio_despues = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo_dispositivo,
                        inventario='dispositivo',
                        periodo__fecha_inicio__lte=fecha_inicio,
                        periodo__fecha_fin__gte=fecha_fin).first()
                    if precio is not None:
                        total_costo_despues = precio_despues.precio * total_despues
                    else:
                        total_costo_despues = 1 * total_despues

                    # fin totales cuando no hay donante
                else:
                    entrada = inv_m.EntradaDetalle.objects.filter(
                        entrada__tipo=tipo_entrada,
                        entrada__fecha_cierre__gte=fecha_inicio,
                        entrada__fecha_cierre__lte=fecha_fin,
                        tipo_dispositivo=tipo_dispositivo,
                        ).exclude(entrada__tipo__nombre='Especial')
                    new_tipo_dispositivo = inv_m.EntradaTipo.objects.get(id=tipo_entrada)
                    altas = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__lte=fecha_inicio,
                        dispositivo__entrada__tipo=tipo_entrada).count()
                    bajas = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=-1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__lte=fecha_inicio,
                        dispositivo__entrada__tipo=tipo_entrada).count()
                    total_final = altas - bajas
                    precio = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo_dispositivo,
                        inventario='dispositivo',
                        periodo__fecha_inicio__lte=fecha_inicio,
                        periodo__fecha_fin__gte=fecha_fin).first()
                    if precio is not None:
                        total_costo = precio.precio * total_final
                    else:
                        total_costo = 1 * total_final
                    # totales
                    altas_despues = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__range=[fecha_inicio, fecha_fin],
                        dispositivo__entrada__tipo=tipo_entrada).count()
                    bajas_despues = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=-1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__range=[fecha_inicio, fecha_fin],
                        dispositivo__entrada__tipo=tipo_entrada).count()
                    total_despues = altas_despues - bajas_despues
                    precio_despues = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo_dispositivo,
                        inventario='dispositivo',
                        periodo__fecha_inicio__lte=fecha_inicio,
                        periodo__fecha_fin__gte=fecha_fin).first()
                    if precio is not None:
                        total_costo_despues = precio_despues.precio * total_despues
                    else:
                        total_costo_despues = 1 * total_despues
                    # fin totales
            else:
                print("si hay donante")
                if(tipo_entrada == 0):
                    entrada = inv_m.EntradaDetalle.objects.filter(
                        entrada__fecha_cierre__gte=fecha_inicio,
                        entrada__fecha_cierre__lte=fecha_fin,
                        tipo_dispositivo=tipo_dispositivo,
                        entrada__proveedor=donante
                        ).exclude(entrada__tipo__nombre='Especial')
                    new_tipo_dispositivo = inv_m.EntradaTipo.objects.all().exclude(nombre='Especial')
                    # totales
                    altas = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__lte=fecha_inicio,
                        dispositivo__entrada__proveedor=donante,
                        ).count()
                    bajas = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=-1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__lte=fecha_inicio,
                        dispositivo__entrada__proveedor=donante,
                        ).count()
                    total_final = altas - bajas
                    precio = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo_dispositivo,
                        inventario='dispositivo',
                        periodo__fecha_inicio__lte=fecha_inicio,
                        periodo__fecha_fin__gte=fecha_fin).first()
                    if precio is not None:
                        total_costo = precio.precio * total_final
                    else:
                        total_costo = 1 * total_final
                    altas_despues = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__range=[fecha_inicio, fecha_fin],
                        dispositivo__entrada__proveedor=donante,
                        ).count()
                    bajas_despues = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=-1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__range=[fecha_inicio, fecha_fin],
                        dispositivo__entrada__proveedor=donante,
                        ).count()
                    total_despues = altas_despues - bajas_despues
                    precio_despues = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo_dispositivo,
                        inventario='dispositivo',
                        periodo__fecha_inicio__lte=fecha_inicio,
                        periodo__fecha_fin__gte=fecha_fin).first()
                    if precio is not None:
                        total_costo_despues = precio_despues.precio * total_despues
                    else:
                        total_costo_despues = 1 * total_despues
                    # fin totales
                else:
                    entrada = inv_m.EntradaDetalle.objects.filter(
                        entrada__tipo=tipo_entrada,
                        entrada__fecha_cierre__gte=fecha_inicio,
                        entrada__fecha_cierre__lte=fecha_fin,
                        tipo_dispositivo=tipo_dispositivo,
                        entrada__proveedor=donante
                        ).exclude(entrada__tipo__nombre='Especial')
                    new_tipo_dispositivo = inv_m.EntradaTipo.objects.get(id=tipo_entrada)
                    altas = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__lte=fecha_inicio,
                        dispositivo__entrada__proveedor=donante,
                        dispositivo__entrada__tipo=tipo_entrada).count()
                    bajas = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=-1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__lte=fecha_inicio,
                        dispositivo__entrada__proveedor=donante,
                        dispositivo__entrada__tipo=tipo_entrada).count()
                    total_final = altas - bajas
                    precio = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo_dispositivo,
                        inventario='dispositivo',
                        periodo__fecha_inicio__lte=fecha_inicio,
                        periodo__fecha_fin__gte=fecha_fin).first()
                    if precio is not None:
                        total_costo = precio.precio * total_final
                    else:
                        total_costo = 1 * total_final
                    altas_despues = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__range=[fecha_inicio, fecha_fin],
                        dispositivo__entrada__proveedor=donante,
                        dispositivo__entrada__tipo=tipo_entrada).count()
                    bajas_despues = conta_m.MovimientoDispositivo.objects.filter(
                        tipo_movimiento=-1,
                        dispositivo__tipo=tipo_dispositivo,
                        fecha__range=[fecha_inicio, fecha_fin],
                        dispositivo__entrada__proveedor=donante,
                        dispositivo__entrada__tipo=tipo_entrada).count()
                    total_despues = altas_despues - bajas_despues
                    precio_despues = conta_m.PrecioEstandar.objects.filter(
                        tipo_dispositivo=tipo_dispositivo,
                        inventario='dispositivo',
                        periodo__fecha_inicio__lte=fecha_inicio,
                        periodo__fecha_fin__gte=fecha_fin).first()
                    if precio is not None:
                        total_costo_despues = precio_despues.precio * total_despues
                    else:
                        total_costo_despues = 1 * total_despues
                    # cantidad = entrada.aggregate(total=Sum('util'))
                    print(entrada.first())
                    # print(cantidad)
            if(new_tipo_dispositivo == "Compra"):
                for datos_entrada in entrada:
                    dispositivo = {}
                    total = datos_entrada.util * datos_entrada.precio_unitario
                    dispositivo['fecha'] = datos_entrada.entrada.fecha
                    dispositivo['id'] = datos_entrada.entrada.id
                    dispositivo['util'] = datos_entrada.util
                    dispositivo['precio'] = datos_entrada.precio_unitario
                    dispositivo['total'] = total
                    dispositivo['tipo'] = datos_entrada.entrada.tipo.nombre
                    dispositivo['proveedor'] = datos_entrada.entrada.proveedor.nombre
                    dispositivo['total_costo'] = total_costo
                    dispositivo['total_final'] = total_final
                    dispositivo['rango_fechas'] = str(fecha_inicio)+" "+str(fecha_fin)
                    dispositivo['tipo_dipositivo'] = new_dispositivo.tipo
                    dispositivo['total_costo_despues'] = total_costo_despues
                    dispositivo['total_despues'] = total_despues
                    lista.append(dispositivo)
            else:
                precio_compra = conta_m.PrecioEstandar.objects.get(
                    tipo_dispositivo=tipo_dispositivo,
                    periodo__actual=True,
                    inventario="dispositivo")
                for datos_entrada in entrada:
                    dispositivo = {}
                    total = datos_entrada.util * precio_compra.precio
                    dispositivo['fecha'] = datos_entrada.entrada.fecha
                    dispositivo['id'] = datos_entrada.entrada.id
                    dispositivo['util'] = datos_entrada.util
                    dispositivo['precio'] = precio_compra.precio
                    dispositivo['total'] = total
                    dispositivo['tipo'] = datos_entrada.entrada.tipo.nombre
                    dispositivo['proveedor'] = datos_entrada.entrada.proveedor.nombre
                    dispositivo['total_costo'] = total_costo
                    dispositivo['total_final'] = total_final
                    dispositivo['rango_fechas'] = str(fecha_inicio)+" "+str(fecha_fin)
                    dispositivo['tipo_dispositivo'] = new_dispositivo.tipo
                    dispositivo['total_costo_despues'] = total_costo_despues
                    dispositivo['total_despues'] = total_despues
                    lista.append(dispositivo)
            # print(lista)
            return Response(lista)
        else:
            print("No existe en el periodo fiscal")
