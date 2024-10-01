from rest_framework import viewsets, generics
from braces.views import CsrfExemptMixin
from apps.cyd import models as cyd_models
from apps.Evaluacion import serializers as eva_serializers

class SedeViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = eva_serializers.SedeSerializer
    queryset = cyd_models.Sede.objects.filter(activa = True)
    filter_fields = ('capacitador', 'municipio','escuela_beneficiada__codigo','fecha_creacion')
