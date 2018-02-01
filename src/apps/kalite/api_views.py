import django_filters
from rest_framework import viewsets, filters

from apps.kalite.serializers import (
    PunteoSerializer, EvaluacionSerializer, VisitaSerializer,
    GradoSerializer, EjerciciosGradoSerializer,
    VisitaCalendarSerializer)

from apps.kalite.models import (
    Punteo, Evaluacion, Visita, Grado, EjerciciosGrado)


class PunteoViewSet(viewsets.ModelViewSet):
    serializer_class = PunteoSerializer
    queryset = Punteo.objects.all()
    filter_fields = ('evaluacion',)


class EvaluacionViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluacionSerializer
    queryset = Evaluacion.objects.all()


class VisitaFilter(filters.FilterSet):

    """Filtros para la visa de :class:`VisitaViewSet`
    """

    fecha_min = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    fecha_max = django_filters.DateFilter(name='fecha', lookup_expr='lte')
    municipio = django_filters.NumberFilter(name='escuela__municipio')
    departamento = django_filters.NumberFilter(name='escuela__municipio__departamento')

    class Meta:
        model = Visita
        fields = ['capacitador', 'fecha_min', 'fecha_max']


class VisitaViewSet(viewsets.ModelViewSet):
    serializer_class = VisitaSerializer
    queryset = Visita.objects.all()
    filter_class = VisitaFilter


class GradoViewSet(viewsets.ModelViewSet):
    serializer_class = GradoSerializer
    queryset = Grado.objects.all()
    filter_fields = ('id', 'visita')


class EjerciciosGradoViewSet(viewsets.ModelViewSet):
    serializer_class = EjerciciosGradoSerializer
    queryset = EjerciciosGrado.objects.all()
    filter_fields = ('id', 'grado')


class CalendarioFilter(filters.FilterSet):

    """Filtros para que permita hacer rangos de fecha
    """

    start = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha', lookup_expr='lte')

    class Meta:
        model = Visita
        fields = ['capacitador', 'escuela', 'fecha', 'start', 'end']


class VisitaCalendarViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaCalendarSerializer
    filter_class = CalendarioFilter
