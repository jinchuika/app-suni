import django_filters
from django_filters import rest_framework as filters

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin

from apps.conta import (
    serializers as conta_s,
    models as conta_m)

from apps.inventario import models as inv_m


class PeriodoFiscalViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informe de la :class:`PeriodoFiscal`
    """
    serializer_class = conta_s.PeriodoFiscalSerializer
    queryset = conta_m.PeriodoFiscal.objects.all()
    filter_fields = ('fecha_inicio', 'fecha_fin', 'actual')

    @action(methods=['post'], detail=False)
    def validar_periodo(self, request, pk=None):
        """ Funcion para validar los periodos fiscales
        """
        fecha_fin = request.data["fecha_fin"]
        fecha_inicio = request.data["fecha_inicio"]
        try:
            actual_checkbox = request.data["actual"]
        except KeyError as e:
            actual_checkbox = 'off'
        if(actual_checkbox == 'on'):
            actual = True
        else:
            actual = False
        periodo_activo = conta_m.PeriodoFiscal.objects.filter(actual=True)
        if periodo_activo.count() >= 1:
            validar_fecha_fin = conta_m.PeriodoFiscal.objects.filter()
            for nuevafecha in validar_fecha_fin:
                if (str(fecha_inicio) >= str(nuevafecha.fecha_fin)) and (str(fecha_fin) > str(fecha_inicio)):
                    print("La fecha no existe")
                else:
                    print("La fecha Existe")
                    return Response(
                        {
                         "Las fechas asignadas ya existen en un periodo fiscal"
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
            for nuevo in periodo_activo:
                nuevo.actual = False
                nuevo.save()
        nuevo_periodo = conta_m.PeriodoFiscal(
            fecha_fin=fecha_fin,
            fecha_inicio=fecha_fin,
            actual=actual
        )
        nuevo_periodo.save()
        return Response(
            {
                'mensaje': 'Actualizacion completa'
            },
            status=status.HTTP_200_OK
        )


class PrecioEstandarViewSet(viewsets.ModelViewSet):
    """ViewSet para generar informe de la :class: `PrecioEstandar`.
    """
    serializer_class = conta_s.PrecioEstandarSerializer
    queryset = conta_m.PrecioEstandar.objects.all()
    filter_fields = ('periodo', 'tipo_dispositivo')

    @action(methods=['post'], detail=False)
    def reevaluar(self, request, pk=None):
        """ Funcion para reevaluar el inventario
        """
        etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
        tipo = request.data['tipo_dispositivo']
        periodo_activo = conta_m.PeriodoFiscal.objects.get(actual=True)
        precios_dispositivo = conta_m.PrecioDispositivo.objects.filter(
            periodo=periodo_activo,
            dispositivo__tipo=tipo).exclude(dispositivo__etapa=etapa)
        precios_repuesto = conta_m.PrecioRepuesto.objects.filter(periodo=periodo_activo,
                                                                 repuesto__tipo=tipo,
                                                                 repuesto__estado=1)
        precios_estandar = conta_m.PrecioEstandar.objects.filter(periodo=periodo_activo,
                                                                 tipo_dispositivo=tipo)
        for estado_dispositivo in precios_dispositivo:
            estado_dispositivo.activo = False
            estado_dispositivo.save()
        for estado_repuesto in precios_repuesto:
            estado_repuesto.activo = False
            estado_repuesto.save()
        for estado_estandar in precios_estandar:
            estado_estandar.activo = False
            estado_estandar.save()
        return Response(
            {
                'mensaje': 'Actualizacion completa'
            },
            status=status.HTTP_200_OK
        )
