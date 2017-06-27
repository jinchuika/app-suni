from django_filters import rest_framework as filters, DateFilter

from braces.views import CsrfExemptMixin
from rest_framework import generics, viewsets

from apps.main.mixins import APIFilterMixin
from apps.cyd.serializers import SedeSerializer, GrupoSerializer, CalendarioSerializer, AsignacionSerializer, ParticipanteSerializer
from apps.cyd.models import Sede, Grupo, Calendario, Asignacion, Participante


class GrupoViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()
    filter_fields = ('sede',)


class CalendarioViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = CalendarioSerializer
    queryset = Calendario.objects.all()
    filter_fields = ('grupo',)


class SedeViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = SedeSerializer
    queryset = Sede.objects.all()
    filter_fields = ('capacitador',)


class AsignacionViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = AsignacionSerializer
    queryset = Asignacion.objects.all()


class ParticipanteViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = ParticipanteSerializer
    queryset = Participante.objects.all()
    filter_fields = ('escuela', 'asignaciones__grupo')


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
