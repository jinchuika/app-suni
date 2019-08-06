from rest_framework import serializers
from django.urls import reverse_lazy

from apps.inventario import models as inv_m


class DesechoDetalleSerializer(serializers.ModelSerializer):
    """ Serializer para generar informes de la :class:'DesechoDetalle'
    """
    tdispositivo = serializers.StringRelatedField(source='entrada_detalle.descripcion', read_only=True)
    entrada = serializers.StringRelatedField(source='entrada_detalle.entrada', read_only=True)

    class Meta:
        model = inv_m.DesechoDetalle
        fields = ['id', 'desecho', 'entrada_detalle', 'cantidad', 'tdispositivo', 'tipo_dispositivo', 'aprobado', 'entrada']

    def validate(self, data):
        errors = {}
        entrada_detalle = data.get('entrada_detalle')
        cantidad = data.get('cantidad')

        if entrada_detalle.existencia_desecho < cantidad:
            errors['error'] = u'Ingrese una cantidad válida'
            raise serializers.ValidationError(errors)
        return data 


class DesechoDispositivoSerializer(serializers.ModelSerializer):
    """ Serializer para generar informes de la :class:'DesechoDispositivo'
    """
    tipo = serializers.StringRelatedField(source='dispositivo.tipo')
    triage = serializers.StringRelatedField(source='dispositivo.triage')

    class Meta:
        model = inv_m.DesechoDispositivo
        fields = '__all__'


class DesechoSalidaSerializer(serializers.ModelSerializer):
    """ Serializer para generar informe de la :class:'DesechoSalida'
    """
    empresa = serializers.StringRelatedField(source='empresa.nombre')
    url_detalle = serializers.SerializerMethodField()
    url_edit = serializers.StringRelatedField(source='get_absolute_url')
    class Meta:
        model = inv_m.DesechoSalida
        fields = ['id','fecha','empresa','en_creacion','url_detalle','url_edit']

    def get_url_detalle(self, obj):
        return reverse_lazy('desechosalida_detail', kwargs={'pk':obj.id})

