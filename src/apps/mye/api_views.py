import django_filters

from rest_framework import viewsets, filters
from django.db.models import Count
from braces.views import LoginRequiredMixin

from apps.escuela import models as escuela_m
from apps.mye import models as mye_m
from apps.mye import serializers as mye_s


class ValidacionCalendarFilter(filters.FilterSet):
    start = django_filters.DateFilter(name='fecha_equipamiento', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha_equipamiento', lookup_expr='lte')

    class Meta:
        model = mye_m.Validacion
        fields = ('start', 'end')


class ValidacionCalendarViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):

    """ViewSet para el widget de calendario en el Home
    de usuarios de TPE.
    """

    serializer_class = mye_s.ValidacionCalendarSerializer
    queryset = mye_m.Validacion.objects.filter(completada=False)
    filter_class = ValidacionCalendarFilter


class MyeFilter(filters.FilterSet):

    """
    Conjunto de filtros para los campos comunes utilizados en
    :class:`SolicitudFilter` y en :class:`ValidacionFilter`.
    """

    escuela = django_filters.ModelChoiceFilter(queryset=escuela_m.Escuela.objects.all())
    codigo = django_filters.CharFilter(name='escuela__codigo')
    departamento = django_filters.NumberFilter(name='escuela__municipio__departamento')
    municipio = django_filters.NumberFilter(name='escuela__municipio')
    nombre = django_filters.CharFilter(name='escuela__nombre', lookup_expr='icontains')
    direccion = django_filters.CharFilter(name='escuela__direccion', lookup_expr='icontains')
    equipada = django_filters.BooleanFilter(method='filter_equipada')
    fecha_min = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    fecha_max = django_filters.DateFilter(name='fecha', lookup_expr='lte')
    alumnos_min = django_filters.NumberFilter(name='poblacion__total_alumno', lookup_expr='gte')
    alumnos_max = django_filters.NumberFilter(name='poblacion__total_alumno', lookup_expr='lte')

    def filter_equipada(self, queryset, name, value):
        if value:
            queryset = queryset.annotate(
                equipamientos=Count('escuela__equipamiento')).filter(equipamientos__gt=0)
        else:
            queryset = queryset.annotate(
                equipamientos=Count('escuela__equipamiento')).filter(equipamientos=0)
        return queryset


class SolicitudFilter(MyeFilter):

    """Filtros para :class:`SolicitudViewSet`
    """

    class Meta:
        model = mye_m.Solicitud
        fields = ('escuela', 'codigo', 'departamento',)


class SolicitudViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):

    """ViewSet para generar listados de :class:`Solicitud`.
    """

    serializer_class = mye_s.SolicitudSerializer
    queryset = mye_m.Solicitud.objects.all()
    filter_class = SolicitudFilter


class ValidacionFilter(MyeFilter):

    """Filtros para :class:`ValidacionViewSet`.
    """

    fecha_min = django_filters.DateFilter(name='fecha_inicio', lookup_expr='gte')
    fecha_max = django_filters.DateFilter(name='fecha_inicio', lookup_expr='lte')
    fecha_tpe_min = django_filters.DateFilter(name='fecha_equipamiento', lookup_expr='gte')
    fecha_tpe_max = django_filters.DateFilter(name='fecha_equipamiento', lookup_expr='lte')
    completada = django_filters.BooleanFilter(name='completada')

    class Meta:
        model = mye_m.Validacion
        fields = ('escuela', 'codigo', 'departamento', 'completada')


class ValidacionViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):

    """ViewSet para generar listados de :class:`Validacion`
    """

    serializer_class = mye_s.ValidacionSerializer
    queryset = mye_m.Validacion.objects.all()
    filter_class = ValidacionFilter
