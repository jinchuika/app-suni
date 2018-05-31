from rest_framework import serializers
from django.urls import reverse_lazy

from apps.inventario import models as inv_m


class DesechoDetalleSerializer(serializers.ModelSerializer):
    """ Serializer para generar informes de la :class:'DesechoDetalle'
    """
    tdispositivo = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.DesechoDetalle
        fields = ['desecho', 'entrada_detalle', 'cantidad', 'tdispositivo']

    def get_tdispositivo(self, object):
        return str(object.tipo_dispositivo)
