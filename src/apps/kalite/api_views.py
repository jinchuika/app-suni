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


class VisitaViewSet(viewsets.ModelViewSet):
    serializer_class = VisitaSerializer
    queryset = Visita.objects.all()


class GradoViewSet(viewsets.ModelViewSet):
    serializer_class = GradoSerializer
    queryset = Grado.objects.all()
    filter_fields = ('id', 'visita')


class EjerciciosGradoViewSet(viewsets.ModelViewSet):
    serializer_class = EjerciciosGradoSerializer
    queryset = EjerciciosGrado.objects.all()
    filter_fields = ('id', 'grado')


class CalendarioFilter(filters.FilterSet):
    start = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha', lookup_expr='lte')

    class Meta:
        model = Visita
        fields = ['capacitador', 'escuela', 'fecha', 'start', 'end']


class VisitaCalendarViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaCalendarSerializer
    filter_class = CalendarioFilter
