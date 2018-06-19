import django_filters
from django_filters import rest_framework as filter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)


class DesechoDetalleViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar los detalles de la :class:`DesechoDetalle`
    """
    serializer_class = inv_s.DesechoDetalleSerializer
    queryset = inv_m.DesechoDetalle.objects.all()
