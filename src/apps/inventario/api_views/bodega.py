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


class TarimaViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informes de :class:`Tarima`
    """
    serializer_class = inv_s.TarimaSerializer
    queryset = inv_m.Tarima.objects.all()


class SectorViewSet(viewsets.ModelViewSet):
    """ViewSet para generar informes de :class:`Sector`
    """
    serializer_class = inv_s.SectorSerializer
    queryset = inv_m.Sector.objects.all()
    filter_fields = ('id', 'nivel',)

    """def partial_update(self, request, *args, **kwargs):
        print(request.data)
        return Response({'status': "Ingreso"})"""
