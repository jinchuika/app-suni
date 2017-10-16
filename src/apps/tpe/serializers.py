from datetime import datetime
from rest_framework import serializers
from apps.tpe.models import (
    Garantia, TicketReparacion, EvaluacionMonitoreo, Monitoreo)


class GarantiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garantia
        fields = '__all__'


class TicketReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReparacion
        fields = '__all__'


class MonitoreoSerializer(serializers.ModelSerializer):
    creado_por = serializers.SerializerMethodField(read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    fecha = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Monitoreo
        fields = '__all__'
        read_only_fields = ('creado_por', 'fecha')

    def get_fecha(self, obj):
        return datetime.now()

    def get_creado_por(self, obj):
        return obj.creado_por.get_full_name()


class EvaluacionMonitoreoSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    porcentaje = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = EvaluacionMonitoreo
        fields = '__all__'
        read_only_fields = ('monitoreo', 'pregunta', 'porcentaje')
