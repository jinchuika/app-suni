from django_filters import rest_framework as filters, DateFilter

from braces.views import CsrfExemptMixin
from rest_framework import generics, viewsets

from apps.main.mixins import APIFilterMixin
from apps.cyd.serializers import GrupoSerializer, CalendarioSerializer
from apps.cyd.models import Grupo, Calendario


class GrupoViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()
    filter_fields = ('sede',)


class CalendarioViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = CalendarioSerializer
    queryset = Calendario.objects.all()
    filter_fields = ('grupo',)


class SaleItemFilter(filters.FilterSet):
    start_date = DateFilter(name='fecha', lookup_expr=('gte'),)
    end_date = DateFilter(name='fecha', lookup_expr=('lte'))

    class Meta:
        model = Calendario
        fields = ['fecha', ]


class CalendarioListAPIView(APIFilterMixin, generics.ListAPIView):
    serializer_class = CalendarioSerializer
    queryset = Calendario.objects.all()
    filter_fields = ('fecha',)
    filter_list = {
        'fecha_inicio': 'fecha__gte',
        'fecha_fin': 'fecha__lte'
    }

    def get_queryset(self):
        queryset = super(CalendarioListAPIView, self).get_queryset()
        return self.filter_queryset(queryset)
