import django_filters

from rest_framework import viewsets, filters
from braces.views import LoginRequiredMixin

from apps.mye import (
    serializers as mye_serializers,
    models as mye_models)

class ValidacionCalendarFilter(filters.FilterSet):
    start = django_filters.DateFilter(name='fecha_equipamiento', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha_equipamiento', lookup_expr='lte')

    class Meta:
        model = mye_models.Validacion
        fields = ('start', 'end')


class ValidacionCalendarViewSet(viewsets.ReadOnlyModelViewSet):

    """ViewSet para el widget de calendario en el Home
    de usuarios de TPE.
    """

    serializer_class = mye_serializers.ValidacionCalendarSerializer
    queryset = mye_models.Validacion.objects.filter(completada=False)
    filter_class = ValidacionCalendarFilter
