import django_filters

from rest_framework import viewsets


from apps.kardex.models import (
    Entrada, EntradaDetalle, Proveedor, Equipo,
    SalidaDetalle, Salida)
from apps.kardex.serializers import (
    EntradaSerializer, EntradaDetalleSerializer, ProveedorSerializer,
    EquipoSerializer, SalidaSerializer, SalidaDetalleSerializer)


class EntradaFilter(django_filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    fecha_fin = django_filters.DateFilter(name='fecha', lookup_expr='lte')
    equipo = django_filters.NumberFilter(name='detalles__equipo')

    class Meta:
        model = Entrada
        fields = ['fecha_inicio', 'fecha_fin', 'proveedor', 'equipo', 'id']


class EntradaViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaSerializer
    queryset = Entrada.objects.all()
    filter_class = EntradaFilter


class EntradaDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaDetalleSerializer
    queryset = EntradaDetalle.objects.all()
    filter_fields = ('entrada', 'equipo',)


class ProveedorViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all()


class EquipoFilter(django_filters.FilterSet):
    equipo = django_filters.NumberFilter(name='id')

    class Meta:
        model = Equipo
        fields = ['equipo', 'id']


class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer
    queryset = Equipo.objects.all()
    filter_class = EquipoFilter

    def get_serializer_context(self):
        """Obtiene los parámetros enviados para filtrar la fecha

        Returns:
            TYPE: dict
        """
        context = super(EquipoViewSet, self).get_serializer_context()
        context['fecha_inicio'] = self.request.query_params.get('fecha_inicio', None)
        context['fecha_fin'] = self.request.query_params.get('fecha_fin', None)
        return context


class SalidaFilter(django_filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    fecha_fin = django_filters.DateFilter(name='fecha', lookup_expr='lte')
    equipo = django_filters.NumberFilter(name='detalles__equipo')

    class Meta:
        model = Salida
        fields = ['fecha_inicio', 'fecha_fin', 'tecnico', 'equipo', 'id']


class SalidaViewSet(viewsets.ModelViewSet):
    serializer_class = SalidaSerializer
    queryset = Salida.objects.all()
    filter_class = SalidaFilter


class SalidaDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = SalidaDetalleSerializer
    queryset = SalidaDetalle.objects.all()
    filter_fields = ('salida', 'equipo',)
