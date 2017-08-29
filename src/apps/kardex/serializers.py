from rest_framework import serializers
from apps.main.serializers import DynamicFieldsModelSerializer

from apps.kardex.models import Entrada, Proveedor


class EntradaSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'


class ProveedorSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
