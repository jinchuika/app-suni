from rest_framework import serializers
from django.urls import reverse_lazy
from apps.recaudacionFondos import models as rf_m
from django.db.models import Sum

class ProveedorSerializer(serializers.ModelSerializer):
    """Serializer para generar los datos que se consumiran en la app de la :class:`Proveedor`
    """
    nombre = serializers.StringRelatedField(allow_null=True)
    entradas = serializers.SerializerMethodField()
    cantidad = serializers.SerializerMethodField()

    class Meta:
        model = rf_m.Proveedor
        fields = [
            'id',
            'nombre',
            'entradas',
            'cantidad']

    def get_entradas(self, obj):
        entradas = rf_m.Entrada.objects.filter(proveedor = obj.id).count()
        return entradas

    def get_cantidad(self, obj):
        entradas = rf_m.Entrada.objects.filter(proveedor = obj.id)
        cantidad  = rf_m.DetalleEntrada.objects.filter(entrada = entradas)
        cantidad_total = 0
        for data in cantidad:
            cantidad_total += data.cantidad
        return cantidad_total

class EntradaSerializer(serializers.ModelSerializer):
    """Serializer para generar los datos que se consumiran en la app de la :class:`Entrada`
    """
    observaciones = serializers.StringRelatedField(allow_null=True)
    fecha = serializers.DateField()
    proveedor = serializers.StringRelatedField()
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = rf_m.Entrada
        fields = [
            'id',
            'observaciones',
            'fecha',
            'proveedor',
             'url']


class ArticuloSerializer(serializers.ModelSerializer):
    """Serializer para generar los datos que se consumiran en la app de la :class:`Entrada`
    """
    nombre = serializers.StringRelatedField(allow_null=True)
    precio = serializers.StringRelatedField()
    categoria = serializers.StringRelatedField()
    entrada = serializers.SerializerMethodField()
    salidas = serializers.SerializerMethodField()
    existencia = serializers.SerializerMethodField()
    entrada_id = serializers.SerializerMethodField()
    proveedor = serializers.SerializerMethodField()
    fecha = serializers.SerializerMethodField()

    class Meta:
        model = rf_m.Articulo
        fields = [
            'id',
            'nombre',
            'precio',
            'categoria',
            'entrada',
            'salidas',
            'existencia',
            'entrada_id',
            'proveedor',
            'fecha']

    def get_entrada(self, obj):
        cantidad = 0
        detalle = rf_m.DetalleEntrada.objects.filter(articulo = obj.id)
        for data in detalle:
            cantidad += data.cantidad
        return cantidad

    def get_salidas(self, obj):
        cantidad = 0
        detalle = rf_m.DetalleSalida.objects.filter(articulo = obj.id)
        for data in detalle:
            cantidad += data.cantidad
        return cantidad
    def get_existencia(self, obj):
        cantidad_entrada = 0
        cantidad_salida =  0
        detalle_entrada = rf_m.DetalleEntrada.objects.filter(articulo = obj.id)
        for data in detalle_entrada:
            cantidad_entrada += data.cantidad
        detalle_salida = rf_m.DetalleSalida.objects.filter(articulo = obj.id)
        for data_salida in detalle_salida:
            cantidad_salida += data_salida.cantidad
        return cantidad_entrada - cantidad_salida

    def get_entrada_id(self, obj):
        detalle_entrada = rf_m.DetalleEntrada.objects.filter(articulo = obj.id)
        id = 0
        for  data in detalle_entrada:
            id = data.entrada.id
        return id

    def get_proveedor(self, obj):
        detalle_entrada = rf_m.DetalleEntrada.objects.filter(articulo = obj.id)
        proveedor = ""
        for  data in detalle_entrada:
            proveedor = data.entrada.proveedor.nombre
        return proveedor

    def get_fecha(self, obj):
        detalle_entrada = rf_m.DetalleEntrada.objects.filter(articulo = obj.id)
        fecha = ""
        for  data in detalle_entrada:
            fecha = data.entrada.fecha
        return fecha


class DetalleEntradaSerializer(serializers.ModelSerializer):
    """Serializer para generar los datos que se consumiran en la app de la :class:`Entrada`
    """
    cantidad = serializers.StringRelatedField()
    caja = serializers.StringRelatedField()
    tarima = serializers.StringRelatedField()
    entrada_id = serializers.StringRelatedField(source = "entrada.id" )
    proveedor = serializers.StringRelatedField(source ="entrada.proveedor")
    fecha = serializers.StringRelatedField(source = "entrada.fecha")

    class Meta:
        model = rf_m.DetalleEntrada
        fields = [
            'cantidad',
            'caja',
            'tarima',
            'entrada_id',
            'proveedor',
            'fecha']

class SalidaSerializer(serializers.ModelSerializer):
    """Serializer para generar los datos que se consumiran en la app de la :class:`Entrada`
    """
    observaciones = serializers.StringRelatedField(allow_null=True)
    #fecha = serializers.DateTimeField(format="%Y-%m-%d")
    fecha = serializers.DateField()
    url = serializers.URLField(source='get_absolute_url')
    tipo = serializers.StringRelatedField()

    class Meta:
        model = rf_m.Salida
        fields = [
            'id',
            'observaciones',
            'fecha',
            'url',
            'tipo']

class DetalleSalidaSerializer(serializers.ModelSerializer):
    """Serializer para generar los datos que se consumiran en la app de la :class:`Entrada`
    """
    cantidad = serializers.StringRelatedField()
    salida_id = serializers.StringRelatedField(source = "salida.id" )
    fecha = serializers.StringRelatedField(source = "salida.fecha")
    tipo = serializers.StringRelatedField(source = "salida.tipo")
    total_salida = serializers.SerializerMethodField()
    class Meta:
        model = rf_m.DetalleSalida
        fields = [
            'cantidad',
            'salida_id',
            'fecha',
            'total_salida',
            'tipo']

    def get_total_salida(self, obj):
        total = obj.precio * obj.cantidad
        return total
