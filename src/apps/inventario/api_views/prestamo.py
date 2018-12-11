import django_filters
from django.db.utils import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)


class PrestamoInformeFilter(filters.FilterSet):
    """ Filtros para la busqueda de Ofertas
    """
    tipo_prestamo = django_filters.CharFilter(name='tipo_prestamo')
    prestado_a = django_filters.CharFilter(name='prestado_a')
    fecha_inicio = django_filters.DateFilter(name='fecha_inicio', method='filter_fecha')
    fecha_fin = django_filters.DateFilter(name='fecha_fin', method='filter_fecha')
    devuelto = django_filters.CharFilter(name='devuelto', method='filter_devuelto')

    class Meta:
        model = inv_m.Prestamo
        fields = ['tipo_prestamo', 'prestado_a', 'fecha_inicio', 'fecha_fin', 'devuelto', ]

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_inicio':
            queryset = queryset.filter(fecha_inicio__gte=value)
        if value and name == 'fecha_fin':
            queryset = queryset.filter(fecha_inicio__lte=value)
        return queryset

    def filter_devuelto(self, queryset, name, value):
        if value == 'True':
            queryset = queryset.filter(devuelto=True)
        else:
            queryset = queryset.filter(devuelto=False)
        return queryset


class PrestamoViewSet(viewsets.ModelViewSet):
    """ViewSet para generar  informe de la :class: `Prestamo`.
    """
    serializer_class = inv_s.PrestamoSerializer
    queryset = inv_m.Prestamo.objects.all()
    filter_class = PrestamoInformeFilter

    @action(methods=['post'], detail=False)
    def devolver_prestamo(self, request, pk=None):
        """Metodo para devolver los dispositivos que fueron prestados
        """
        id_prestamo = request.data['prestamo']
        prestamo = inv_m.Prestamo.objects.get(id=id_prestamo)
        etapa_bodega = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.AB)
        estado_pendiente = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        for asignacion in prestamo.dispositivo.all():
            dispositivo = inv_m.Dispositivo.objects.get(triage=asignacion.triage)
            dispositivo.etapa = etapa_bodega
            dispositivo.estado = estado_pendiente
            dispositivo.save()
        prestamo.devuelto = True
        prestamo.fecha_fin = datetime.now()
        prestamo.save()
        return Response(
                {
                    'mensaje': 'Prestamo Devuelto'
                },
                status=status.HTTP_200_OK
            )
