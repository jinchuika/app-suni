import django_filters

from django.db.models import Count
from rest_framework import viewsets

from apps.users.models import Organizacion
from apps.escuela.models import Escuela

from apps.ie import models as ie_models
from apps.ie.serializers import (
    OrganizacionSerializer, LaboratorioSerializer,
    EscuelaSerializer, GeografiaSerializer)


class OrganizacionViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizacionSerializer
    queryset = Organizacion.objects.all()


class LaboratorioViewSet(viewsets.ModelViewSet):
    serializer_class = LaboratorioSerializer
    queryset = ie_models.Laboratorio.objects.all()


class EscuelaViewSet(viewsets.ModelViewSet):
    serializer_class = EscuelaSerializer
    queryset = Escuela.objects.annotate(labs=Count('laboratorios')).filter(labs__gt=0, mapa__isnull=False)


class GeografiaViewSet(viewsets.ModelViewSet):
    serializer_class = GeografiaSerializer
    queryset = Escuela.objects.values(
        'municipio__departamento__nombre',
        'sector__sector',
        'nivel__nivel',
        'area__area').annotate(cantidad=Count('id')).filter(status__id=1)
