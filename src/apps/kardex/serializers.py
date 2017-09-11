from rest_framework import serializers
from apps.main.serializers import DynamicFieldsModelSerializer

from apps.kardex.models import Entrada, Proveedor, Equipo, SalidaDetalle, Salida


class EquipoSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    cantidad_entrada = serializers.IntegerField()
    cantidad_salida = serializers.IntegerField()
    existencia = serializers.IntegerField()

    class Meta:
        model = Equipo
        fields = '__all__'


class EntradaSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    equipo = serializers.StringRelatedField()
    proveedor = serializers.StringRelatedField()
    tipo = serializers.StringRelatedField()
    estado = serializers.StringRelatedField()

    class Meta:
        model = Entrada
        fields = '__all__'


class ProveedorSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class SalidaSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = Salida
        fields = '__all__'


class SalidaDetalleSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = SalidaDetalle
        fields = '__all__'
