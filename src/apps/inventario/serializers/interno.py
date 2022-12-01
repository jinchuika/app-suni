from rest_framework import serializers
from django.urls import reverse_lazy
from apps.inventario import models as inv_m
from .bodega import DispositivoSerializer

class InventarioInternoSerializer(serializers.ModelSerializer):
    """Serializer para la :class: `InventarioInterno`"""
    no_asignacion = serializers.StringRelatedField()
    colaborador_asignado = serializers.StringRelatedField(source='colaborador_asignado.get_full_name')
    creada_por = serializers.StringRelatedField(source='creada_por.get_full_name')
    estado = serializers.StringRelatedField()
    no_dispositivos = serializers.SerializerMethodField()
    url = serializers.StringRelatedField(source='get_absolute_url')
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.InventarioInterno
        fields = '__all__'

    def get_detail_url(self, object):
        return reverse_lazy('inventariointerno_detail', kwargs={'pk': object.id})

    def get_no_dispositivos(self, object):
        dispositivos_asignados = inv_m.IInternoDispositivo.objects.filter(no_asignacion=object.id)
        return len(dispositivos_asignados)

class IInternoDispositivoSerializer(serializers.ModelSerializer):

    no_asignacion = InventarioInternoSerializer()
    dispositivo = DispositivoSerializer()
    asignado_por = serializers.StringRelatedField(source='asignado_por.get_full_name')
    asignacion_dispositivo = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.IInternoDispositivo
        fields = '__all__'

    def get_asignacion_dispositivo(self, object):
        return '{no_asignacion}-{indice}'.format(no_asignacion=object.no_asignacion, indice=object.indice)