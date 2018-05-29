import django_filters
from django_filters import rest_framework as filters

from rest_framework import viewsets
from braces.views import LoginRequiredMixin

from apps.crm import (
    serializers as crm_s,
    models as crm_m)


class OfertasInformeFilter(filters.FilterSet):
    """ Filtros para la busqueda de Ofertas
    """
    donante = django_filters.CharFilter(name='donante')
    tipo_oferta = django_filters.CharFilter(name='tipo_oferta')
    fecha_min = django_filters.DateFilter(name='fecha_min', method='filter_fecha')
    fecha_max = django_filters.DateFilter(name='fecha_max', method='filter_fecha')

    class Meta:
        model = crm_m.Oferta
        fields = ['donante', 'tipo_oferta', 'fecha_min', 'fecha_max']

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_min':
            queryset = queryset.filter(fecha_inicio__gte=value)
        if value and name == 'fecha_max':
            queryset = queryset.filter(fecha_inicio__lte=value)
        return queryset


class OfertaViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = crm_s.ofertaSerializer
    queryset = crm_m.Oferta.objects.all()
    filter_class = OfertasInformeFilter
