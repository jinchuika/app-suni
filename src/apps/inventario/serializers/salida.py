from rest_framework import serializers
from django.urls import reverse_lazy
from apps.inventario import models as inv_m


class SalidaInventarioSerializer(serializers.ModelSerializer):
    """docstring for SalidaInventarioSerializer."""
    class Meta:
        model = inv_m.SalidaInventario
        fields = '__all__'
