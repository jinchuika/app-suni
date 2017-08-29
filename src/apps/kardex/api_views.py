from rest_framework import viewsets


from apps.kardex.models import (
    Entrada, Proveedor)
from apps.kardex.serializers import EntradaSerializer, ProveedorSerializer


class EntradaViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaSerializer
    queryset = Entrada.objects.all()
    filter_fields = ('proveedor',)


class ProveedorViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all()
