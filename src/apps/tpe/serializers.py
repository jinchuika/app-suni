from rest_framework import serializers
from apps.tpe.models import Garantia, TicketReparacion, EvaluacionMonitoreo


class GarantiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garantia
        fields = '__all__'


class TicketReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReparacion
        fields = '__all__'


class EvaluacionMonitoreoSerializer(serializers.ModelSerializer):
    porcentaje = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = EvaluacionMonitoreo
        fields = '__all__'
        read_only_fields = ('monitoreo', 'pregunta', 'porcentaje')
