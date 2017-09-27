from rest_framework import serializers
from apps.main.serializers import DynamicFieldsModelSerializer

from apps.kardex.models import (
    Entrada, Proveedor, Equipo, SalidaDetalle, Salida, EntradaDetalle)


class EquipoSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    cantidad_entrada = serializers.SerializerMethodField()
    cantidad_salida = serializers.SerializerMethodField()
    inventario_entrada = serializers.SerializerMethodField()
    inventario_salida = serializers.SerializerMethodField()
    existencia = serializers.IntegerField()

    class Meta:
        model = Equipo
        fields = '__all__'

    def get_cantidad_entrada(self, obj):
        """Para obtener la cantidad de :model:`kardex.EntradaDetalle`
        en el rango de fechas seleccionado. Depende del contexto
        enviado por la vista, recibe `fecha_inicio` o `fecha_salida`
        como parámetros opcionales.

        Returns:
            TYPE: int
        """
        queryset = obj.detalles_entrada.all()
        if self.context['fecha_inicio']:
            queryset = queryset.filter(entrada__fecha__gte=self.context['fecha_inicio'])
        if self.context['fecha_fin']:
            queryset = queryset.filter(entrada__fecha__lte=self.context['fecha_fin'])
        return queryset.count()

    def get_cantidad_salida(self, obj):
        """Para obtener la cantidad de :model:`kardex.SalidaDetalle`
        en el rango de fechas seleccionado. Depende del contexto
        enviado por la vista, recibe `fecha_inicio` o `fecha_salida`
        como parámetros opcionales.

        Returns:
            TYPE: int
        """
        queryset = obj.detalles_salida.all()
        if self.context['fecha_inicio']:
            queryset = queryset.filter(salida__fecha__gte=self.context['fecha_inicio'])
        if self.context['fecha_fin']:
            queryset = queryset.filter(salida__fecha__lte=self.context['fecha_fin'])
        return queryset.count()

    def get_inventario_entrada(self, obj):
        """Para obtener la cantidad de equipo ingresado por medio
        de las :model:`kardex.EntradaDetalle` en un rango de fechas determinado.
        Depende de los parámetros de contexto opcionales `fecha_inicio`
        y `fecha_salida`.

        Returns:
            TYPE: int
        """
        queryset = obj.detalles_entrada.all()
        if self.context['fecha_inicio']:
            queryset = queryset.filter(entrada__fecha__gte=self.context['fecha_inicio'])
        if self.context['fecha_fin']:
            queryset = queryset.filter(entrada__fecha__lte=self.context['fecha_fin'])
        return sum(detalle.cantidad for detalle in queryset)

    def get_inventario_salida(self, obj):
        """Para obtener la cantidad de equipo que ha salido por medio
        de :model:`kardex.SalidaDetalle` en un rango de fechas determinado.
        Depende de los parámetros de contexto opcionales `fecha_inicio`
        y `fecha_salida`.

        Returns:
            TYPE: int
        """
        queryset = obj.detalles_salida.all()
        if self.context['fecha_inicio']:
            queryset = queryset.filter(salida__fecha__gte=self.context['fecha_inicio'])
        if self.context['fecha_fin']:
            queryset = queryset.filter(salida__fecha__lte=self.context['fecha_fin'])
        return sum(detalle.cantidad for detalle in queryset)


class EntradaSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    proveedor = serializers.StringRelatedField()
    tipo = serializers.StringRelatedField()
    estado = serializers.StringRelatedField()
    url = serializers.URLField(source='get_absolute_url')
    precio_total = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)

    class Meta:
        model = Entrada
        fields = '__all__'


class EntradaDetalleSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    fecha = serializers.DateField(source='entrada.fecha')
    entrada_url = serializers.URLField(source='entrada.get_absolute_url')

    class Meta:
        model = EntradaDetalle
        fields = '__all__'


class ProveedorSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class SalidaSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')
    tecnico = serializers.CharField(source='tecnico.get_full_name')

    class Meta:
        model = Salida
        fields = '__all__'


class SalidaDetalleSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    fecha = serializers.DateField(source='salida.fecha')
    salida_url = serializers.URLField(source='salida.get_absolute_url')

    class Meta:
        model = SalidaDetalle
        fields = '__all__'
