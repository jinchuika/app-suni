import django_filters

from rest_framework import viewsets, filters
from django.db.models import Count, Sum
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


class EvaluacionFilter(filters.FilterSet):

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


class SolicitudFilter(EvaluacionFilter):

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


class ValidacionFilter(EvaluacionFilter):

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


class CooperanteFilter(filters.FilterSet):
    equipamientos_min = django_filters.NumberFilter(name='equipamientos_min', method='filter_equipamientos')
    equipamientos_max = django_filters.NumberFilter(name='equipamientos_max', method='filter_equipamientos')
    equipo_min = django_filters.NumberFilter(name='equipo_min', method='filter_equipo')
    equipo_max = django_filters.NumberFilter(name='equipo_max', method='filter_equipo')
    fecha_min = django_filters.DateFilter(name='fecha_min', method='filter_fecha')
    fecha_max = django_filters.DateFilter(name='fecha_max', method='filter_fecha')

    class Meta:
        model = mye_m.Cooperante
        fields = ['equipamientos_min', 'equipamientos_max', 'equipo_min', 'equipo_max', 'fecha_min', 'fecha_max']

    def filter_equipamientos(self, queryset, name, value):
        if value and name == 'equipamientos_min':
            queryset = queryset.annotate(cantidad=Count('equipamientos')).filter(cantidad__gte=value)
        if value and name == 'equipamientos_max':
            queryset = queryset.annotate(cantidad=Count('equipamientos')).filter(cantidad__lte=value)
        return queryset

    def filter_equipo(self, queryset, name, value):
        if value and name == 'equipo_min':
            queryset = queryset.annotate(cantidad=Sum('equipamientos__cantidad_equipo')).filter(cantidad__gte=value)
        if value and name == 'equipo_max':
            queryset = queryset.annotate(cantidad=Sum('equipamientos__cantidad_equipo')).filter(cantidad__lte=value)
        return queryset

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_min':
            queryset = queryset.filter(equipamientos__fecha__gte=value)
        if value and name == 'fecha_max':
            queryset = queryset.filter(equipamientos__fecha__lte=value)
        return queryset


class CooperanteViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = mye_s.CooperanteSerializer
    queryset = mye_m.Cooperante.objects.all()
    filter_class = CooperanteFilter


class ProyectoFilter(filters.FilterSet):
    cantidad_equipamientos = django_filters.NumberFilter(name='cantidad_equipamientos', method='filter_equipamiento')
    fecha_min = django_filters.DateFilter(name='fecha_min', method='filter_fecha')
    fecha_max = django_filters.DateFilter(name='fecha_max', method='filter_fecha')

    class Meta:
        model = mye_m.Proyecto
        fields = ['cantidad_equipamientos', 'fecha_min', 'fecha_max']

    def filter_equipamiento(self, queryset, name, value):
        if value and name == 'cantidad_equipamientos':
            queryset = queryset.annotate(cantidad=Count('equipamientos')).filter(cantidad__gte=value)
        if value and name == 'equipamientos_max':
            queryset = queryset.annotate(cantidad=Count('equipamientos')).filter(cantidad__lte=value)
        return queryset

    def filter_fecha(self, queryset, name, value):

        if value and name == 'fecha_min':

            queryset = queryset.filter(equipamientos__fecha__gte=value)

        if value and name == 'fecha_max':
            queryset = queryset.filter(equipamientos__fecha__lte=value)
        return queryset


class ProyectoViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = mye_s.ProyectoSerializer
    queryset = mye_m.Proyecto.objects.all()
    filter_class = ProyectoFilter
