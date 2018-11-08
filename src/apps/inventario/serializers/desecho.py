from rest_framework import serializers
from django.urls import reverse_lazy

from apps.inventario import models as inv_m


class DesechoDetalleSerializer(serializers.ModelSerializer):
    """ Serializer para generar informes de la :class:'DesechoDetalle'
    """
    tdispositivo = serializers.StringRelatedField(source='tipo_dispositivo', read_only=True)

    class Meta:
        model = inv_m.DesechoDetalle
        fields = ['id', 'desecho', 'entrada_detalle', 'cantidad', 'tdispositivo', 'tipo_dispositivo', 'aprobado']


class DesechoDispositivoSerializer(serializers.ModelSerializer):
    """ Serializer para generar informes de la :class:'DesechoDetalle'
    """
    tipo = serializers.StringRelatedField(source='dispositivo.tipo')
    triage = serializers.StringRelatedField(source='dispositivo.triage')

    class Meta:
        model = inv_m.DesechoDispositivo
        fields = '__all__'
