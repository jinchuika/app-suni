import django_filters
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)


class DetalleInformeFilter(filters.FilterSet):
    """ Filtro para generar los informes por entrada
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
