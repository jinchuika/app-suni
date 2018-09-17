from django.db.utils import OperationalError

import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)


class DetalleInformeFilter(filters.FilterSet):
    """ Filtro para generar los informes de Detalles de Entrada
    """
    tipo = django_filters.CharFilter(name='entrada')

    class Meta:
        model = inv_m.EntradaDetalle
        fields = ['entrada']


class EntradaDetalleViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar las tablas de la :class:'EntradaDetalle'
    """
    serializer_class = inv_s.EntradaDetalleSerializer
    queryset = inv_m.EntradaDetalle.objects.all()
    filter_class = DetalleInformeFilter

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    @action(methods=['post'], detail=False)
    def cuadrar_salida(self, request, pk=None):
        entrad_id = request.data['primary_key']
        entrada = inv_m.EntradaDetalle.objects.filter(entrada=entrad_id)
        dispositivo_repuestos = inv_m.EntradaDetalle.objects.filter(entrada=entrad_id).count()
        validar_dispositivos = inv_m.EntradaDetalle.objects.filter(entrada=entrad_id,
                                                                   dispositivos_creados=True).count()
        validar_repuestos = inv_m.EntradaDetalle.objects.filter(entrada=entrad_id,
                                                                repuestos_creados=True).count()
        print("Total detalles:" + str(dispositivo_repuestos))
        print("Total repuestos creados:" + str(validar_repuestos))
        print("Total dispositivos creados:" + str(validar_dispositivos))
        for detalles in entrada:
            total_detalle = detalles.util + detalles.repuesto + detalles.desecho
            print("total acumulado :" + str(total_detalle))
            print("total:" + str(detalles.total))
            if(detalles.total != total_detalle):
                print("La entrada no esta cuadrada")
                return Response(
                    {'mensaje': 'La entrada no esta cuadrada'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                print("La entrada esta cuadrada")
                if(dispositivo_repuestos != validar_dispositivos or dispositivo_repuestos != validar_repuestos):
                    print("Los Dispositivos no han sido creados")
                    return Response(
                        {'mensaje': 'Los dispositivos o repuestos no  han sido creados'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    print("Los dispositivos o repuesto han sido creados ")
        return Response(
            {'mensaje': 'Entrada Cuadrada'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=True)
    def crear_dispositivos(self, request, pk=None):
        entrada_detalle = self.get_object()
        try:
            creacion = entrada_detalle.crear_dispositivos()
            validar_dispositivos = inv_m.EntradaDetalle.objects.get(id=pk)
            validar_dispositivos.dispositivos_creados = True
            validar_dispositivos.save()
            return Response(
                creacion,
                status=status.HTTP_200_OK)
        except OperationalError as e:
            return Response(
                {'mensaje': str(e)},
                status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def crear_repuestos(self, request, pk=None):
        entrada_detalle = self.get_object()
        try:
            creacion = entrada_detalle.crear_repuestos()
            validar_dispositivos = inv_m.EntradaDetalle.objects.get(id=pk)
            validar_dispositivos.repuestos_creados = True
            validar_dispositivos.save()
            return Response(
                creacion,
                status=status.HTTP_200_OK
            )
        except OperationalError as e:
            return Response(
                {'mensaje': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class EntradaFilter(filters.FilterSet):
    """ Filtros para generar informe de Entrada
    """

    proveedor = django_filters.CharFilter(name='proveedor')
    tipo = django_filters.CharFilter(name='tipo')
    recibida_por = django_filters.CharFilter(name='recibida_por')
    fecha_min = django_filters.DateFilter(name='fecha_min', method='filter_fecha')
    fecha_max = django_filters.DateFilter(name='fecha_max', method='filter_fecha')

    class Meta:
        model = inv_m.Entrada
        fields = ['proveedor', 'tipo', 'recibida_por', 'fecha_min', 'fecha_max']

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_min':
            queryset = queryset.filter(fecha__gte=value)
        if value and name == 'fecha_max':
            queryset = queryset.filter(fecha__lte=value)
        return queryset


class EntradaViewSet(viewsets.ModelViewSet):
    """ Serializer para generar las tablas de la :class:'Entrada'
    """
    serializer_class = inv_s.EntradaSerializer
    queryset = inv_m.Entrada.objects.all()
    filter_class = EntradaFilter
