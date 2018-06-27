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


class DispositivoFilter(filters.FilterSet):
    """Filtros para el ViewSet de Disositivo"""
    buscador = filters.CharFilter(name='buscador', method='filter_buscador')

    class Meta:
        model = inv_m.Dispositivo
        fields = ('tarima', 'id', 'etapa', 'estado', 'tipo', 'triage')

    def filter_buscador(self, qs, name, value):
        return qs.filter(triage__istartswith=value)


class DispositivoViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informes de :class:`Dispositivo`
    """
    serializer_class = inv_s.DispositivoSerializer
    queryset = inv_m.Dispositivo.objects.all()
    filter_class = DispositivoFilter

    @action(methods=['get'], detail=False)
    def paquete(self, request, pk=None):
        """Encargada de filtrar los dispositivos que puedan ser elegidos para asignarse a `Paquete`"""
        queryset = inv_m.Dispositivo.objects.filter(
            estado=inv_m.DispositivoEstado.BN,
            etapa=inv_m.DispositivoEtapa.TR
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
