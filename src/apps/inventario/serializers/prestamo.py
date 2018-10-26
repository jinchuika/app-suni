from rest_framework import serializers
from django.urls import reverse_lazy
from apps.inventario import models as inv_m


class PrestamoSerializer(serializers.ModelSerializer):
    """Serializer para generar los datos que se mostraran de la :class:`Prestamos`
    """
    prestado_a = serializers.StringRelatedField(source='prestado_a.get_full_name')
    dispositivo = serializers.StringRelatedField(source='dispositivo.triage')
    tipo_dispositivo = serializers.StringRelatedField(source='tipo_dispositivo.tipo')
    tipo_prestamo = serializers.StringRelatedField(source='tipo_prestamo.nombre')

    class Meta:
        model = inv_m.Prestamo
        fields = '__all__'
