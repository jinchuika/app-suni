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
    """ Serializer para generar las tablas de la :class:'EntradaDetalle'
    """
    serializer_class = inv_s.EntradaDetalleSerializer
    queryset = inv_m.EntradaDetalle.objects.all()
    filter_class = DetalleInformeFilter

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    @action(methods=['post'], detail=True)
    def crear_dispositivos(self, request, pk=None):
        entrada_detalle = self.get_object()
        try:
            creacion = entrada_detalle.crear_dispositivos()
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
