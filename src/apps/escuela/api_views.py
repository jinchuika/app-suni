from braces.views import CsrfExemptMixin
from rest_framework import viewsets

from apps.escuela.models import Escuela
from apps.escuela.serializers import EscuelaSerializer


class EscuelaViewSet(viewsets.ModelViewSet):
    queryset = Escuela.objects.all()
    serializer_class = EscuelaSerializer
    filter_fields = ('codigo', 'municipio', 'municipio__departamento', 'nivel', 'sector')
