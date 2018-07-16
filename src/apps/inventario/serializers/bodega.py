from rest_framework import serializers
from django.urls import reverse_lazy
from apps.inventario import models as inv_m


class DispositivoSerializer(serializers.ModelSerializer):
    """Serializer para generar los datos que se consumiran en la app de la :class:`Dispositivo`
    """
    tipo = serializers.StringRelatedField()
    estado = serializers.StringRelatedField()
    etapa = serializers.StringRelatedField()
    marca = serializers.StringRelatedField()
    modelo = serializers.StringRelatedField()
    serie = serializers.StringRelatedField()

    class Meta:
        model = inv_m.Dispositivo
        fields = [
            'id',
            'triage',
            'tipo',
            'entrada',
            'estado',
            'etapa',
            'marca',
            'modelo',
            'serie',
            'tarima']


class TarimaSerializer(serializers.ModelSerializer):
    """ Serializer para generar los datos del app  de la :class:`Tarima`
    """
    dispositivos = DispositivoSerializer(many=True)
    cantidad_dispositivos = serializers.IntegerField(source='dispositivos.count')

    class Meta:
        model = inv_m.Tarima
        fields = ['sector', 'codigo_qr', 'dispositivos', 'cantidad_dispositivos']


class SectorSerializer(serializers.ModelSerializer):
    """ Serializer para  generar los datos para app de la :class:`Sector`
    """
    id = serializers.StringRelatedField(source='__str__')
    dispositivos = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.Sector
        fields = ['id', 'sector', 'nivel', 'dispositivos']

    def get_dispositivos(self, obj, pk=None):
        lista_dispositivos = inv_m.Dispositivo.objects.filter(tarima__sector=obj)
        dispositivos_s = DispositivoSerializer(lista_dispositivos, many=True)
        return dispositivos_s.data
