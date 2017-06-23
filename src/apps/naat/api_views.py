from django.db.models import Count
from django.contrib.auth.models import User

from braces.views import CsrfExemptMixin
from rest_framework import viewsets, generics

from apps.cyd.models import Participante
from apps.naat.models import AsignacionNaat
from apps.naat.serializers import AsignacionNaatSerializer, ParticipanteNaatSerializer, FacilitadorNaatSerializer


class AsignacionNaatViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = AsignacionNaatSerializer
    queryset = AsignacionNaat.objects.all()


class FacilitadorListView(generics.ListAPIView):
    serializer_class = FacilitadorNaatSerializer
    queryset = User.objects.filter(groups__name='naat_facilitador')


class FacilitadorRetrieveView(generics.RetrieveAPIView):
    serializer_class = FacilitadorNaatSerializer
    queryset = User.objects.filter(groups__name='naat_facilitador')
    lookup_field = 'username'


class ParticipanteListView(generics.ListAPIView):
    serializer_class = ParticipanteNaatSerializer
    queryset = Participante.objects.annotate(num_asignaciones_naat=Count('asignaciones_naat')).filter(num_asignaciones_naat__gt=0)


class ParticipanteRetrieveView(generics.RetrieveAPIView):
    serializer_class = ParticipanteNaatSerializer
    queryset = Participante.objects.annotate(num_asignaciones_naat=Count('asignaciones_naat')).filter(num_asignaciones_naat__gt=0)
    lookup_field = 'dpi'


class ParticipanteUpdateView(generics.UpdateAPIView):
    serializer_class = ParticipanteNaatSerializer
    queryset = Participante.objects.annotate(num_asignaciones_naat=Count('asignaciones_naat')).filter(num_asignaciones_naat__gt=0)
    lookup_field = 'dpi'


class AsignacionNaatListView(generics.ListAPIView):
    serializer_class = AsignacionNaatSerializer
    queryset = AsignacionNaat.objects.all()


class AsignacionNaatRetrieveView(generics.RetrieveAPIView):
    serializer_class = AsignacionNaatSerializer
    queryset = AsignacionNaat.objects.all()
    lookup_field = 'dpi'
