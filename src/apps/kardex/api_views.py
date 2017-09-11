from rest_framework import viewsets


from apps.kardex.models import (
    Entrada, Proveedor, Equipo, SalidaDetalle, Salida)
from apps.kardex.serializers import (
    EntradaSerializer, ProveedorSerializer, EquipoSerializer,
    SalidaSerializer, SalidaDetalleSerializer)


class EntradaViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaSerializer
    queryset = Entrada.objects.all()
    filter_fields = ('proveedor', 'id')


class ProveedorViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all()


class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer
    queryset = Equipo.objects.all()


class SalidaViewSet(viewsets.ModelViewSet):
    serializer_class = SalidaSerializer
    queryset = Salida.objects.all()
    filter_fields = ('id',)


class SalidaDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = SalidaDetalleSerializer
    queryset = SalidaDetalle.objects.all()
