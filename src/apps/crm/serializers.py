from rest_framework import serializers

from apps.main.serializers import DynamicFieldsModelSerializer
from apps.crm import models as crm_m


class ofertaSerializer(serializers.ModelSerializer):
    """Serializer para generar informes completos de :class:`Oferta`
    """
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    urlDonante = serializers.URLField(source='donante.get_absolute_url')
    id = serializers.IntegerField()
    recibido = serializers.SerializerMethodField()
    fecha_inicio = serializers.DateField()
    fecha_bodega = serializers.DateField()
    fecha_carta = serializers.DateField()
    donante = serializers.CharField()
    tipo_oferta = serializers.CharField()
    contable = serializers.SerializerMethodField()

    class Meta:
        model = crm_m.Oferta
        fields = (
            'url',
            'urlDonante',
            'id',
            'contable',
            'recibido',
            'fecha_inicio',
            'fecha_bodega',
            'fecha_carta',
            'donante',
            'tipo_oferta')

    def get_recibido(self, object):
        return object.recibido_por.get_full_name()

    def get_contable(self, object):
        respuesta = object.recibo_contable
        responder = ""
        if respuesta:
            responder = "Si"
        else:
            responder = "No"

        return responder


class DonanteSerializer(serializers.ModelSerializer):
    """ Serializer para generar informes completos de :class:`Donante`
    """
    class Meta:
        model = crm_m.Donante
        fields = (
            'id',
            'nombre'
        )
