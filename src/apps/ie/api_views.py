import django_filters
from django_filters import rest_framework as filters
from django.db.models import Count
from rest_framework import viewsets

from braces.views import LoginRequiredMixin

from apps.users.models import Organizacion
from apps.escuela.models import Escuela

from apps.ie import models as ie_models
from apps.ie import serializers as ie_serializers


class DashOrganizacionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ie_serializers.DashOrganizacionSerializer
    queryset = Organizacion.objects.all()


class DashLaboratorioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ie_serializers.DashLaboratorioSerializer
    queryset = ie_models.Laboratorio.objects.values(
        'cantidad_computadoras',
        'escuela__municipio__departamento__nombre',
        'escuela__area__area',
        'organizacion__nombre',
        'poblacion__alumna',
        'poblacion__alumno',
        'fecha').all()


class DashEscuelaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ie_serializers.DashEscuelaSerializer
    queryset = Escuela.objects.annotate(labs=Count('laboratorios')).filter(labs__gt=0, mapa__isnull=False)


class DashGeografiaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ie_serializers.DashGeografiaSerializer
    queryset = Escuela.objects.values(
        'municipio__departamento__nombre',
        'sector__sector',
        'nivel__nivel',
        'area__area').annotate(cantidad=Count('id')).filter(status__id=1)


class GenericFilter(filters.FilterSet):

    """Filtros para que permita hacer rangos de fecha
    """

    fecha_inicio = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    fecha_fin = django_filters.DateFilter(name='fecha', lookup_expr='lte')
    codigo = django_filters.CharFilter(name='escuela__codigo',)
    municipio = django_filters.NumberFilter(name='escuela__municipio')
    departamento = django_filters.NumberFilter(name='escuela__municipio__departamento')


class LaboratorioFilter(GenericFilter):
    class Meta:
        model = ie_models.Laboratorio
        fields = ['organizacion']


class ValidacionFilter(filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(name='fecha_inicio', lookup_expr='gte')
    fecha_fin = django_filters.DateFilter(name='fecha_fin', lookup_expr='lte')
    codigo = django_filters.CharFilter(name='escuela__codigo',)
    municipio = django_filters.NumberFilter(name='escuela__municipio')
    departamento = django_filters.NumberFilter(name='escuela__municipio__departamento')

    class Meta:
        model = ie_models.Validacion
        fields = ['organizacion']


class LaboratorioViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    """ViewSet para generar informes de laboratorios"""
    serializer_class = ie_serializers.LaboratorioSerializer
    filter_class = LaboratorioFilter

    def get_queryset(self):
        is_super = self.request.user.is_superuser
        not_org = self.request.user.perfil.organizacion is None

        if (is_super or not_org):
            return ie_models.Laboratorio.objects.all()
        else:
            return ie_models.Laboratorio.objects.filter(
                organizacion=self.request.user.perfil.organizacion)


class IEValidacionViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    """ViewSet para generar informes de laboratorios"""
    serializer_class = ie_serializers.IEValidacionSerializer
    filter_class = ValidacionFilter

    def get_queryset(self):
        is_super = self.request.user.is_superuser
        not_org = self.request.user.perfil.organizacion is None

        if (is_super or not_org):
            return ie_models.Validacion.objects.all()
        else:
            return ie_models.Validacion.objects.filter(
                organizacion=self.request.user.perfil.organizacion)
