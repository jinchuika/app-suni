from rest_framework import viewsets


from apps.kardex.models import (
    Entrada, Proveedor, Equipo)
from apps.kardex.serializers import (
    EntradaSerializer, ProveedorSerializer, EquipoSerializer)


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
