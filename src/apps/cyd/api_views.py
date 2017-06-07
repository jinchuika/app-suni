from braces.views import CsrfExemptMixin
from rest_framework import mixins, generics, viewsets

from apps.cyd.serializers import GrupoSerializer, CalendarioSerializer
from apps.cyd.models import Grupo, Calendario


class GrupoViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()


class CalendarioViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = CalendarioSerializer
    queryset = Calendario.objects.all()
