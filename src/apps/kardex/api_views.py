from rest_framework import viewsets


from apps.kardex.models import (
    Entrada, EntradaDetalle, Proveedor, Equipo,
    SalidaDetalle, Salida)
from apps.kardex.serializers import (
    EntradaSerializer, EntradaDetalleSerializer, ProveedorSerializer,
    EquipoSerializer, SalidaSerializer, SalidaDetalleSerializer)


class EntradaViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaSerializer
    queryset = Entrada.objects.all()
    filter_fields = ('proveedor', 'id')


class EntradaDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaDetalleSerializer
    queryset = EntradaDetalle.objects.all()
    filter_fields = ('entrada', 'equipo',)


class ProveedorViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all()


class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer
    queryset = Equipo.objects.all()
    filter_fields = ('id',)

    def get_serializer_context(self):
        """Obtiene los parámetros enviados para filtrar la fecha

        Returns:
            TYPE: dict
        """
        context = super(EquipoViewSet, self).get_serializer_context()
        context['fecha_inicio'] = self.request.query_params.get('fecha_inicio', None)
        context['fecha_fin'] = self.request.query_params.get('fecha_fin', None)
        return context


class SalidaViewSet(viewsets.ModelViewSet):
    serializer_class = SalidaSerializer
    queryset = Salida.objects.all()
    filter_fields = ('id',)


class SalidaDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = SalidaDetalleSerializer
    queryset = SalidaDetalle.objects.all()
    filter_fields = ('salida', 'equipo',)
