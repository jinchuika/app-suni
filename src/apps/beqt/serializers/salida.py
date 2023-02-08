from rest_framework import serializers
from django.urls import reverse_lazy
#from apps.inventario import models as inv_m
from apps.beqt import models as beqt_m

class SalidaInventarioSerializer(serializers.ModelSerializer):
    """Serializer para la :class: `SalidaInventario`"""
    tipo_salida = serializers.StringRelatedField()
    beneficiario = serializers.StringRelatedField()
    estado = serializers.StringRelatedField()
    url = serializers.StringRelatedField(source='get_absolute_url')
    escuela = serializers.StringRelatedField(source='escuela.codigo')
    detail_url = serializers.SerializerMethodField()
    escuela_url = serializers.StringRelatedField(source='escuela.get_absolute_url')

    class Meta:
        model = beqt_m.SalidaInventario
        fields = '__all__'

    def get_detail_url(self, object):
        return reverse_lazy('salidainventario_beqt_detail', kwargs={'pk': object.id})


class RevisionSalidaSerializer(serializers.ModelSerializer):
    """ Serializer para la :class:`RevisionSalida`
    """
    revisado_por = serializers.StringRelatedField(source='revisado_por.get_full_name')
    urlSalida = serializers.StringRelatedField(source='get_absolute_url')
    estado = serializers.StringRelatedField(source='salida.estado')
    no_salida = serializers.StringRelatedField(source='salida.no_salida')
    escuela_url = serializers.StringRelatedField(source='salida.escuela.get_absolute_url')
    escuela = serializers.StringRelatedField(source='salida.escuela.codigo')
    tipo_salida = serializers.StringRelatedField(source='salida.tipo_salida')
    beneficiario = serializers.StringRelatedField(source='salida.beneficiario')

    class Meta:
        model = beqt_m.RevisionSalidaBeqt
        fields = '__all__'
