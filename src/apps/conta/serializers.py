from rest_framework import serializers
from apps.main.serializers import DynamicFieldsModelSerializer
from apps.conta import models as conta_m


class PeriodoFiscalSerializer(serializers.ModelSerializer):
    """ Serializer para la :class: `PeriodoFiscal`
    """
    class Meta:
        model = conta_m.PeriodoFiscal
        fields = '__all__'


class PrecioEstandarSerializer(serializers.ModelSerializer):
    """Serializer para la :class: `PrecioEstandar`
    """
    id_dispositivo = serializers.StringRelatedField(source='tipo_dispositivo')
    creado_por = serializers.StringRelatedField(source='creado_por.get_full_name')
    periodo = serializers.StringRelatedField(source='periodo.__str__')

    class Meta:
        model = conta_m.PrecioEstandar
        fields = '__all__'
