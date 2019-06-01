from rest_framework import serializers
from django.urls import reverse_lazy
from apps.inventario import models as inv_m


class SalidaInventarioSerializer(serializers.ModelSerializer):
    """Serializer para la :class: `SalidaInventario`"""
    tipo_salida = serializers.StringRelatedField()
    beneficiario = serializers.StringRelatedField()
    estado = serializers.StringRelatedField()
    url = serializers.StringRelatedField(source='get_absolute_url')
    escuela = serializers.StringRelatedField(source='escuela.codigo')
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.SalidaInventario
        fields = '__all__'

    def get_detail_url(self, object):
        return reverse_lazy('salidainventario_detail', kwargs={'pk': object.id})


class RevisionSalidaSerializer(serializers.ModelSerializer):
    """ Serializer para la :class:`RevisionSalida`
    """
    revisado_por = serializers.StringRelatedField(source='revisado_por.get_full_name')
    urlSalida = serializers.StringRelatedField(source='get_absolute_url')
    estado = serializers.StringRelatedField(source='salida.estado')
    no_salida = serializers.StringRelatedField(source='salida.no_salida')

    class Meta:
        model = inv_m.RevisionSalida
        fields = '__all__'
