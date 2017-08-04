from braces.views import CsrfExemptMixin
from rest_framework import generics, viewsets

from apps.main.mixins import APIFilterMixin
from apps.cyd.serializers import (
    SedeSerializer, GrupoSerializer, CalendarioSerializer,
    AsignacionSerializer, ParticipanteSerializer,
    NotaAsistenciaSerializer, NotaHitoSerializer, AsesoriaSerializer)
from apps.cyd.models import (
    Sede, Grupo, Calendario, Asignacion, Participante,
    NotaAsistencia, NotaHito, Asesoria)


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
    """La diferencia con ParticipanteViewSet es que este usa el DPI como primary key
    """
    serializer_class = ParticipanteSerializer
    queryset = Participante.objects.all()
    filter_fields = ('escuela', 'asignaciones__grupo', 'dpi')
    lookup_field = 'dpi'


class ParticipanteAPIViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    """La diferencia con ParticipanteViewSet es que este ViewSet se basa en el ID
    """
    serializer_class = ParticipanteSerializer
    queryset = Participante.objects.all()
    filter_fields = ('escuela', 'asignaciones__grupo', 'dpi')


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


class NotaAsistenciaViewSet(viewsets.ModelViewSet):
    serializer_class = NotaAsistenciaSerializer
    queryset = NotaAsistencia.objects.all()
    filter_fields = ('asignacion',)


class NotaHitoViewSet(viewsets.ModelViewSet):
    serializer_class = NotaHitoSerializer
    queryset = NotaHito.objects.all()
    filter_fields = ('asignacion',)


class AsesoriaViewSet(viewsets.ModelViewSet):
    serializer_class = AsesoriaSerializer
    queryset = Asesoria.objects.all()
    filter_fields = ('sede', 'sede__capacitador',)
