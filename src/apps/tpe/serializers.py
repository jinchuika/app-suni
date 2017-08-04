from rest_framework import serializers
from apps.tpe.models import Garantia, TicketReparacion


class GarantiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garantia
        fields = '__all__'


class TicketReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReparacion
        fields = '__all__'
