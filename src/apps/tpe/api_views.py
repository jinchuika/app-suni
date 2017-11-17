import django_filters
from datetime import datetime

from rest_framework import viewsets, filters
from braces.views import LoginRequiredMixin

from apps.mye import models as mye_models
from apps.tpe import (
    serializers as tpe_serializers,
    models as tpe_models)


class TicketReparacionViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = tpe_serializers.TicketReparacionSerializer
    queryset = tpe_models.TicketReparacion.objects.all()
    filter_fields = (
        'ticket',
        'tecnico_asignado',
        'estado',
        'triage',
        'tipo_dispositivo',
        'ticket__garantia__equipamiento__escuela')


class MonitoreoViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = tpe_serializers.MonitoreoSerializer
    queryset = tpe_models.Monitoreo.objects.all()
    filter_fields = ('equipamiento', 'equipamiento__escuela')

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user, fecha=datetime.today())


class EvaluacionMonitoreoViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = tpe_serializers.EvaluacionMonitoreoSerializer
    queryset = tpe_models.EvaluacionMonitoreo.objects.all()
    filter_fields = ('monitoreo', 'pregunta')


class EquipamientoFilter(filters.FilterSet):
    codigo = django_filters.CharFilter(name='escuela__codigo')
    fecha_min = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    fecha_max = django_filters.DateFilter(name='fecha', lookup_expr='lte')
    municipio = django_filters.NumberFilter(name='escuela__municipio')
    departamento = django_filters.NumberFilter(name='escuela__municipio__departamento')
    nivel = django_filters.NumberFilter(name='escuela__nivel')
    renovacion = django_filters.BooleanFilter(name='renovacion')
    equipamiento_id = django_filters.NumberFilter(name='id')
    cooperante = django_filters.ModelMultipleChoiceFilter(queryset=mye_models.Cooperante.objects.all())
    proyecto = django_filters.ModelMultipleChoiceFilter(queryset=mye_models.Proyecto.objects.all())
    nombre = django_filters.CharFilter(name='escuela__nombre', lookup_expr='icontains')

    class Meta:
        model = tpe_models.Equipamiento
        fields = (
            'codigo',
            'fecha_min',
            'fecha_max',
            'municipio',
            'departamento',
            'nivel',
            'renovacion',
            'equipamiento_id',
            'cooperante',
            'proyecto')


class EquipamientoViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = tpe_serializers.EquipamientoSerializer
    queryset = tpe_models.Equipamiento.objects.all()
    filter_class = EquipamientoFilter
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)


class EquipamientoFullViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = tpe_serializers.EquipamientoFullSerializer
    queryset = tpe_models.Equipamiento.objects.all()
    filter_class = EquipamientoFilter
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)


class EquipamientoCalendarFilter(filters.FilterSet):
    start = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha', lookup_expr='lte')

    class Meta:
        model = tpe_models.Equipamiento
        fields = ('start', 'end')


class EquipamientoCalendarViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):

    """Para generar el listado de `Equipamiento`s en
    la página de inicio.
    """
    
    serializer_class = tpe_serializers.EquipamientoCalendarSerializer
    queryset = tpe_models.Equipamiento.objects.all()
    filter_class = EquipamientoCalendarFilter
