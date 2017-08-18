from braces.views import CsrfExemptMixin
from rest_framework import viewsets

from apps.main.models import Departamento, Municipio
from apps.main import serializers as main_serializers


class DepartamentoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = main_serializers.DepartamentoSerializer
    queryset = Departamento.objects.all()


class MunicipioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = main_serializers.MunicipioSerializer
    queryset = Municipio.objects.all()
    filter_fields = ('departamento',)
