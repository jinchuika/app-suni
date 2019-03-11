import django_filters
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, views
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
        # Obtener data a Operar
        data_id = request.data['id']

        precio_estandar = conta_m.PrecioEstandar.objects.get(pk=data_id)
        
        if precio_estandar.inventario == conta_m.PrecioEstandar.DISPOSITIVO:
            utiles = inv_m.Dispositivo.objects.filter(valido=True, tipo=precio_estandar.tipo_dispositivo)
            for dispositivo in utiles:
                # Obtener y Desactivar Precios Anteriores
                precios_anteriores = conta_m.PrecioDispositivo.objects.filter(dispositivo=dispositivo, activo=True)
                validar_precio = len(precios_anteriores.filter(periodo=precio_estandar.periodo)) == 0
                if len(precios_anteriores.filter(periodo=precio_estandar.periodo)) == 0:
                    if dispositivo.entrada.tipo.contable == False:
                        for precio in precios_anteriores:
                            precio.activo = False
                            precio.save()

                        # Generar nuevo precio de periodo actual
                        nuevo_precio = conta_m.PrecioDispositivo(
                            dispositivo=dispositivo,
                            periodo=precio_estandar.periodo,
                            precio=precio_estandar.precio
                            )
                        nuevo_precio.save()
        else:
            utiles = inv_m.Repuesto.objects.filter(valido=True, tipo=precio_estandar.tipo_dispositivo)
            for repuesto in utiles:
                # Obtener y Desactivar Precios Anteriores
                precios_anteriores = conta_m.PrecioRepuesto.objects.filter(repuesto=repuesto, activo=True)
                if len(precios_anteriores.filter(periodo=precio_estandar.periodo)) == 0:
                    if repuesto.entrada.tipo.contable == False:
                        for precio in precios_anteriores:
                            precio.activo = False
                            precio.save()

                        # Generar nuevo precio de periodo actual
                        nuevo_precio = conta_m.PrecioRepuesto(
                            repuesto=repuesto,
                            periodo=precio_estandar.periodo,
                            precio=precio_estandar.precio
                            )
                        nuevo_precio.save()

        precio_estandar.revaluar = True
        precio_estandar.save()

        return Response(
            {
                'mensaje': 'Actualizacion completa'
            },
            status=status.HTTP_200_OK
        )


class PeriodoFiscalPorExistenciaViewSet(viewsets.ModelViewSet):
    """ViewSet para generar informe de la :class: `PrecioEstandar`.
    """
    # serializer_class = conta_s.PeriodoFiscalPorExistenciaSerializer
    serializer_class = conta_s.DispositivosContaSerializer
    # queryset = conta_m.PeriodoFiscal.objects.filter(actual=True)
    # queryset = conta_m.MovimientoDispositivo.objects.all()
    queryset = inv_m.Dispositivo.objects.all()
    # filter_fields = ('periodo_fiscal', 'dispositivo__tipo', )


class PruebaJson(views.APIView):
    def get(self, request):
        return Response({'some': 'data'})

    @classmethod
    def get_extra_actions(cls):
        return []
