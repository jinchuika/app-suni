from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.main.serializers import DynamicFieldsModelSerializer
from apps.conta import models as conta_m
from apps.inventario import models as inv_m
from dateutil.relativedelta import relativedelta


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


class PeriodoFiscalPorExistenciaSerializer(serializers.ModelSerializer):
    """Serializer para la :class: `PrecioEstandar`
    """
    cantidad = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    tipo = serializers.StringRelatedField(source='dispositivo.tipo')

    class Meta:
        model = conta_m.MovimientoDispositivo
        fields = ('cantidad', 'precio', 'tipo', 'total')

    def get_cantidad(self, obj, pk=None):
        tipo_dispositivo = inv_m.DispositivoTipo.objects.all()
        altas = conta_m.MovimientoDispositivo.objects.filter(
            tipo_movimiento=1,
            ).count()
        bajas = conta_m.MovimientoDispositivo.objects.filter(
            tipo_movimiento=-1,
            ).count()
        disponible = altas - bajas
        return disponible

    def get_total(self, obj, pk=None):
        altas = conta_m.MovimientoDispositivo.objects.filter(tipo_movimiento=1).count()
        bajas = conta_m.MovimientoDispositivo.objects.filter(tipo_movimiento=-1).count()
        disponible = altas - bajas
        total = disponible * 0.2
        return total


class DispositivosContaSerializer(serializers.ModelSerializer):
    tipo = serializers.StringRelatedField(allow_null=True)
    dispositivo = PeriodoFiscalPorExistenciaSerializer(many=True)

    class Meta:
        model = inv_m.Dispositivo
        fields = ['tipo', 'dispositivo']
