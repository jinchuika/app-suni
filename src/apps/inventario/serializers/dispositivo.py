from rest_framework import serializers
from django.urls import reverse_lazy
from apps.inventario import models as inv_m
from .bodega import DispositivoSerializer


class DispositivoPaqueteSerializer(serializers.ModelSerializer):
    """ Serializer para generar los datos que se mostraran de la :class:`DispositivoPaquete`
    """
    dispositivo = DispositivoSerializer()

    class Meta:
        model = inv_m.DispositivoPaquete
        fields = '__all__'


class PaqueteSerializer(serializers.ModelSerializer):
    """ Serializer para generar los datos que se mostraran de la :class:`Paquete`
    """
    asignacion = DispositivoPaqueteSerializer(many=True)
    id = serializers.StringRelatedField(source='__str__')
    id_paquete = serializers.StringRelatedField(source='id')
    tipo_paquete = serializers.StringRelatedField()
    urlPaquet = serializers.StringRelatedField(source='get_absolute_url')
    cantidad_dispositivos = serializers.SerializerMethodField()
    tipo_salida = serializers.StringRelatedField(source='salida.tipo_salida')

    class Meta:
        model = inv_m.Paquete
        fields = (
            'urlPaquet',
            'id_paquete',
            'id',
            'fecha_creacion',
            'indice',
            'aprobado',
            'salida',
            'creado_por',
            'tipo_paquete',
            'cantidad_dispositivos',
            'tipo_salida',
            'cantidad',
            'asignacion'

            )

    def get_cantidad_dispositivos(self, obj, pk=None):
        numero_dispositivos = inv_m.DispositivoPaquete.objects.filter(paquete=obj).count()
        print(numero_dispositivos)
        print(obj)
        return numero_dispositivos
