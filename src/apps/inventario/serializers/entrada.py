from rest_framework import serializers
from django.urls import reverse_lazy

from apps.inventario import models as inv_m


class EntradaDetalleSerializer(serializers.ModelSerializer):
    """ Serializer para generar informes de la :class:'EntradaDetalle'
    """

    tdispositivo = serializers.SerializerMethodField()
    tipo_entrada = serializers.StringRelatedField(source='entrada.tipo')
    usa_triage = serializers.StringRelatedField(source='tipo_dispositivo.usa_triage')
    # Campos contabilidad
    precio_unitario = serializers.DecimalField(max_digits=8, decimal_places=2, default=None)
    precio_descontado = serializers.DecimalField(max_digits=8, decimal_places=2, default=None)
    precio_total = serializers.DecimalField(max_digits=10, decimal_places=2, default=None)
    # Registro
    creado_por = serializers.StringRelatedField(source='creado_por.get_full_name')
    update_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = inv_m.EntradaDetalle
        fields = (
            'id',
            'entrada',
            'tipo_dispositivo',
            'util',
            'repuesto',
            'desecho',
            'total',
            'precio_unitario',
            'precio_subtotal',
            'precio_descontado',
            'precio_total',
            'creado_por',
            'tdispositivo',
            'update_url',
            'tipo_entrada',
            'dispositivos_creados',
            'repuestos_creados',
            'descripcion',
            'usa_triage'
        )

    def get_tdispositivo(self, object):
        return object.tipo_dispositivo.__str__()

    def get_update_url(self, object):
        return reverse_lazy('entradadetalle_update', kwargs={'pk': object.id})


class EntradaSerializer(serializers.ModelSerializer):
    """ Serializer para generar el infome de la `class`:`Entrada`
    """
    creada_por = serializers.StringRelatedField(source='creada_por.get_full_name')
    recibida_por = serializers.StringRelatedField(source='recibida_por.get_full_name')
    proveedor = serializers.StringRelatedField()
    en_creacion = serializers.SerializerMethodField()
    boton = serializers.StringRelatedField(source='creada_por.get_full_name')
    tipo = serializers.StringRelatedField()
    urlSi = serializers.StringRelatedField(source='get_absolute_url')
    urlNo = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.Entrada
        fields = (
            'id',
            'tipo',
            'fecha',
            'en_creacion',
            'creada_por',
            'recibida_por',
            'proveedor',
            'boton',
            'urlSi',
            'urlNo',
        )

    def get_en_creacion(sel, object):
        if object.en_creacion:
            return "Si"
        else:
            return "No"

    def get_urlNo(self, object):
        return reverse_lazy('entrada_detail', kwargs={'pk': object.id})
