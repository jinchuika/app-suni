import django_filters

from rest_framework import viewsets, filters
from django.db.models import Count
from braces.views import LoginRequiredMixin

from apps.escuela.models import Escuela
from apps.mye import (
    serializers as mye_serializers,
    models as mye_models)


class ValidacionCalendarFilter(filters.FilterSet):
    start = django_filters.DateFilter(name='fecha_equipamiento', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha_equipamiento', lookup_expr='lte')

    class Meta:
        model = mye_models.Validacion
        fields = ('start', 'end')


class ValidacionCalendarViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):

    """ViewSet para el widget de calendario en el Home
    de usuarios de TPE.
    """

    serializer_class = mye_serializers.ValidacionCalendarSerializer
    queryset = mye_models.Validacion.objects.filter(completada=False)
    filter_class = ValidacionCalendarFilter


class SolicitudFilter(filters.FilterSet):

    """Filtros para :class:`SolicitudViewSet`
    """

    escuela = django_filters.ModelChoiceFilter(queryset=Escuela.objects.all())
    codigo = django_filters.CharFilter(name='escuela__codigo')
    departamento = django_filters.NumberFilter(name='escuela__municipio__departamento')
    municipio = django_filters.NumberFilter(name='escuela__municipio')
    nombre = django_filters.CharFilter(name='escuela__nombre', lookup_expr='icontains')
    direccion = django_filters.CharFilter(name='escuela__direccion', lookup_expr='icontains')
    equipada = django_filters.BooleanFilter(method='filter_equipada')
    fecha_min = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    fecha_max = django_filters.DateFilter(name='fecha', lookup_expr='lte')
    alumnos_min = django_filters.DateFilter(name='poblacion__total_alumno', lookup_expr='gte')
    alumnos_max = django_filters.DateFilter(name='poblacion__total_alumno', lookup_expr='lte')

    def filter_equipada(self, queryset, name, value):
        if value:
            queryset = queryset.annotate(
                equipamientos=Count('escuela__equipamiento')).filter(equipamientos__gt=0)
        else:
            queryset = queryset.annotate(
                equipamientos=Count('escuela__equipamiento')).filter(equipamientos=0)
        return queryset

    class Meta:
        model = mye_models.Solicitud
        fields = ('escuela', 'codigo', 'departamento', 'fecha_max', 'fecha_min')


class SolicitudViewSet(viewsets.ReadOnlyModelViewSet):

    """ViewSet para generar listados de :class:`Solicitud`
    """

    serializer_class = mye_serializers.SolicitudSerializer
    queryset = mye_models.Solicitud.objects.all()
    filter_class = SolicitudFilter
