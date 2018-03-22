from django.db.models import Count
from django.contrib.auth.models import User

import django_filters
from braces.views import CsrfExemptMixin
from rest_framework import viewsets, filters, generics

from apps.cyd.models import Participante
from apps.naat import models as naat_m
from apps.naat import serializers as naat_s
from apps.naat.views import BaseNaatPermission


class AsignacionNaatViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = naat_s.AsignacionNaatSerializer
    queryset = naat_m.AsignacionNaat.objects.all()


class FacilitadorListView(generics.ListAPIView):
    serializer_class = naat_s.FacilitadorNaatSerializer
    queryset = User.objects.filter(groups__name='naat_facilitador')


class FacilitadorRetrieveView(generics.RetrieveAPIView):
    serializer_class = naat_s.FacilitadorNaatSerializer
    queryset = User.objects.filter(groups__name='naat_facilitador')
    lookup_field = 'username'


class ParticipanteListView(generics.ListAPIView):
    serializer_class = naat_s.ParticipanteNaatSerializer
    queryset = Participante.objects.annotate(
        num_asignaciones_naat=Count('asignaciones_naat')).filter(num_asignaciones_naat__gt=0)


class ParticipanteRetrieveView(generics.RetrieveAPIView):
    serializer_class = naat_s.ParticipanteNaatSerializer
    queryset = Participante.objects.annotate(
        num_asignaciones_naat=Count('asignaciones_naat')).filter(num_asignaciones_naat__gt=0)
    lookup_field = 'dpi'


class ParticipanteUpdateView(generics.UpdateAPIView):
    serializer_class = naat_s.ParticipanteNaatSerializer
    queryset = Participante.objects.annotate(
        num_asignaciones_naat=Count('asignaciones_naat')).filter(num_asignaciones_naat__gt=0)
    lookup_field = 'dpi'


class AsignacionNaatListView(generics.ListAPIView):
    serializer_class = naat_s.AsignacionNaatSerializer
    queryset = naat_m.AsignacionNaat.objects.all()


class AsignacionNaatRetrieveView(generics.RetrieveAPIView):
    serializer_class = naat_s.AsignacionNaatSerializer
    queryset = naat_m.AsignacionNaat.objects.all()
    lookup_field = 'dpi'


class CalendarioFilter(filters.FilterSet):

    """Filtros para que permita hacer rangos de fecha
    """

    start = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha', lookup_expr='lte')

    class Meta:
        model = naat_m.SesionPresencial
        fields = ['fecha', 'start', 'end']


class SesionPresencialCalendarViewSet(BaseNaatPermission, viewsets.ModelViewSet):
    queryset = naat_m.SesionPresencial.objects.all()
    serializer_class = naat_s.SesionCalendarSerializer
    filter_class = CalendarioFilter
