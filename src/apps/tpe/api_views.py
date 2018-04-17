import django_filters
from datetime import datetime
from django.db.models import Count

from rest_framework import viewsets, filters
from braces.views import LoginRequiredMixin

from apps.mye import models as mye_m
from apps.tpe import (
    serializers as tpe_serializers,
    models as tpe_m)


class TicketReparacionViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = tpe_serializers.TicketReparacionSerializer
    queryset = tpe_m.TicketReparacion.objects.all()
    filter_fields = (
        'ticket',
        'tecnico_asignado',
        'estado',
        'triage',
        'tipo_dispositivo',
        'ticket__garantia__equipamiento__escuela')


class MonitoreoViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = tpe_serializers.MonitoreoSerializer
    queryset = tpe_m.Monitoreo.objects.all()
    filter_fields = ('equipamiento', 'equipamiento__escuela')

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user, fecha=datetime.today())


class EvaluacionMonitoreoViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = tpe_serializers.EvaluacionMonitoreoSerializer
    queryset = tpe_m.EvaluacionMonitoreo.objects.all()
    filter_fields = ('monitoreo', 'pregunta')


class EvaluacionMonitoreoFilter(filters.FilterSet):
    creado_por = django_filters.CharFilter(name='monitoreo__creado_por')
    fecha_min = django_filters.DateFilter(name='monitoreo__fecha', lookup_expr='gte')
    fecha_max = django_filters.DateFilter(name='monitoreo__fecha', lookup_expr='lte')

    class Meta:
        model = tpe_m.EvaluacionMonitoreo
        fields = ('creado_por', 'fecha_max', 'fecha_min',)


class EvaluacionMonitoreoFullViewSet(LoginRequiredMixin, viewsets.ModelViewSet):

    """ViewSet para generar informes de :class:`EvaluacionMonitoreo`
    """

    serializer_class = tpe_serializers.EvaluacionMonitoreoFullSerializer
    queryset = tpe_m.EvaluacionMonitoreo.objects.all()
    filter_class = EvaluacionMonitoreoFilter


class EquipamientoFilter(filters.FilterSet):
    codigo = django_filters.CharFilter(name='escuela__codigo')
    fecha_min = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    fecha_max = django_filters.DateFilter(name='fecha', lookup_expr='lte')
    municipio = django_filters.NumberFilter(name='escuela__municipio')
    departamento = django_filters.NumberFilter(name='escuela__municipio__departamento')
    nivel = django_filters.NumberFilter(name='escuela__nivel')
    renovacion = django_filters.BooleanFilter(name='renovacion')
    equipamiento_id = django_filters.NumberFilter(name='id')
    cooperante = django_filters.ModelMultipleChoiceFilter(queryset=mye_m.Cooperante.objects.all())
    proyecto = django_filters.ModelMultipleChoiceFilter(queryset=mye_m.Proyecto.objects.all())
    nombre = django_filters.CharFilter(name='escuela__nombre', lookup_expr='icontains')

    class Meta:
        model = tpe_m.Equipamiento
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
    queryset = tpe_m.Equipamiento.objects.all()
    filter_class = EquipamientoFilter
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)


class EquipamientoFullViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = tpe_serializers.EquipamientoFullSerializer
    queryset = tpe_m.Equipamiento.objects.all()
    filter_class = EquipamientoFilter
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)


class EquipamientoCalendarFilter(filters.FilterSet):
    start = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha', lookup_expr='lte')

    class Meta:
        model = tpe_m.Equipamiento
        fields = ('start', 'end')


class EquipamientoCalendarViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):

    """Para generar el listado de `Equipamiento`s en
    la página de inicio.
    """

    serializer_class = tpe_serializers.EquipamientoCalendarSerializer
    queryset = tpe_m.Equipamiento.objects.all()
    filter_class = EquipamientoCalendarFilter


class DispositivoReparacionFilter(filters.FilterSet):

    """Filtros para usar en el ViewSet de
    :class:`DispositivoReparacionViewSet`
    """

    fecha_min = django_filters.DateFilter(name='fecha_fin', lookup_expr='gte')
    fecha_max = django_filters.DateFilter(name='fecha_fin', lookup_expr='lte')

    class Meta:
        model = tpe_m.TicketReparacion
        fields = ('fecha_min', 'fecha_max')


class DispositivoReparacionViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):

    """Para listar los la cantidad de :class:`DispositivoReparacion`es creadas
    para cada :class:`TicketReparacion`.
    """
    serializer_class = tpe_serializers.DispositivoReparacionSerializar
    queryset = tpe_m.TicketReparacion.objects.values(
        'tipo_dispositivo', 'tipo_dispositivo__tipo').annotate(
        total=Count('id'))
    filter_class = DispositivoReparacionFilter


class VisitaMonitoreoFilter(filters.FilterSet):

    """Filtros para usar en el ViewSet de
    :class:`VisitaMonitoreoViewset`
    """

    start = django_filters.DateFilter(name='fecha_visita', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha_visita', lookup_expr='lte')

    class Meta:
        model = tpe_m.VisitaMonitoreo
        fields = ('start', 'end')


class VisitaMonitoreoInformeFilter(filters.FilterSet):
    """ Filtros para la busqueda en monitoreo de visitas
    """
    fecha_visita = django_filters.DateFilter(name='fecha_visita')
    departamento = django_filters.NumberFilter(name='equipamiento__escuela__municipio__departamento',)
    municipio = django_filters.NumberFilter(name='equipamiento__escuela__municipio')
    encargado = django_filters.CharFilter(name='encargado')
    fecha_min = django_filters.DateFilter(name='fecha_min', method='filter_fecha')
    fecha_max = django_filters.DateFilter(name='fecha_max', method='filter_fecha')

    class Meta:
        model = tpe_m.VisitaMonitoreo
        fields = ['fecha_visita', 'municipio', 'departamento', 'encargado', 'fecha_min', 'fecha_max']

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_min':
            queryset = queryset.filter(fecha_visita__gte=value)
        if value and name == 'fecha_max':
            queryset = queryset.filter(fecha_visita__lte=value)
        return queryset


class VisitaMonitoreoCalendarViewset(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    """Vista encargada de  manipular el calendario
    """
    serializer_class = tpe_serializers.VisitaMonitoreoCalendarSerializer
    queryset = tpe_m.VisitaMonitoreo.objects.all()
    filter_class = VisitaMonitoreoFilter


class VisitaMonitoreoViewset(LoginRequiredMixin, viewsets.ModelViewSet):
    """Para generar el listado del monitoreo de visitas
    """
    serializer_class = tpe_serializers.VisitaMonitoreoSerializer
    queryset = tpe_m.VisitaMonitoreo.objects.all()
    filter_class = VisitaMonitoreoInformeFilter
