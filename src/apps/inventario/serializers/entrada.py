from rest_framework import serializers

from apps.inventario import models as inv_m


class EntradaDetalleSerializer(serializers.ModelSerializer):
    """ Serializer para generar informes de la :class:'EntradaDetalle'
    """
    tdispositivo = serializers.SerializerMethodField()
    # Campos contabilidad
    precio_unitario = serializers.DecimalField(max_digits=8, decimal_places=2, default=None)
    precio_descontado = serializers.DecimalField(max_digits=8, decimal_places=2, default=None)
    precio_total = serializers.DecimalField(max_digits=10, decimal_places=2, default=None)
    # Registro
    creado_por = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.EntradaDetalle
        fields = (
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
            'tdispositivo'

        )

    def get_creado_por(self, object):
        return object.creado_por.get_full_name()

    def get_tdispositivo(self, object):
        return object.tipo_dispositivo.__str__()
