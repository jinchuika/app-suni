from rest_framework import serializers
from django.urls import reverse_lazy
from apps.beqt import models as beqt_m
from .bodega import DispositivoSerializer
from django.core import serializers as serializers_django


class DispositivoPaqueteSerializer(serializers.ModelSerializer):
    """ Serializer para generar los datos que se mostraran de la :class:`DispositivoPaquete`
    """
    dispositivo = DispositivoSerializer()

    class Meta:
        model = beqt_m.DispositivoPaquete
        fields = ('dispositivo', )


class DispositivoPaqueteSerializerConta(serializers.ModelSerializer):
    """ Serializer para generar los datos que se mostraran de la :class:`DispositivoPaquete`
    en el area de contabilidad
    """
    salida = serializers.StringRelatedField(source='paquete.salida')
    dispositivo = serializers.StringRelatedField(source='dispositivo.triage')
    etapa = serializers.StringRelatedField(source='dispositivo.etapa')
    tipo = serializers.StringRelatedField(source='dispositivo.tipo')
    asignado_por = serializers.StringRelatedField(source='asignado_por.get_full_name')
    paquete = serializers.StringRelatedField(source='paquete.__str__')

    class Meta:
        model = beqt_m.DispositivoPaquete
        fields = '__all__'


class PaqueteSerializer(serializers.ModelSerializer):
    """ Serializer para generar los datos que se mostraran de la :class:`Paquete`
    """
    asignacion = DispositivoPaqueteSerializer(source='asignacion_beqt',many=True)
    id = serializers.StringRelatedField(source='__str__')
    id_paquete = serializers.StringRelatedField(source='id')
    tipo_paquete = serializers.StringRelatedField()
    usa_triage = serializers.StringRelatedField(source='tipo_paquete.tipo_dispositivo.usa_triage')
    urlPaquet = serializers.StringRelatedField(source='get_absolute_url')
    cantidad_dispositivos = serializers.SerializerMethodField()
    tipo_salida = serializers.StringRelatedField(source='salida.tipo_salida')
    url_detail = serializers.SerializerMethodField()

    class Meta:
        model = beqt_m.PaqueteBeqt
        fields = (
            'urlPaquet',
            'id_paquete',
            'id',
            'fecha_creacion',
            'indice',
            'aprobado',
            'salida',
            'creado_por',
            'tipo_paquete',
            'cantidad_dispositivos',
            'tipo_salida',
            'cantidad',
            'url_detail',
            'usa_triage',
            'aprobado_kardex',
            'desactivado',
            'asignacion'

            )

    def get_cantidad_dispositivos(self, obj, pk=None):
        numero_dispositivos = beqt_m.DispositivoPaquete.objects.filter(paquete=obj).count()
        return numero_dispositivos

    def get_url_detail(self, obj):
        return reverse_lazy('dispositivo_beqt_asignados', kwargs={'pk': obj.id})

class SolicitudMovimientoSerializer(serializers.ModelSerializer):
    """ Serializer para generar los datos que se mostraran de la :class:`SolicitudMovimiento`
    """
    creada_por = serializers.StringRelatedField(source='creada_por.get_full_name')
    autorizada_por = serializers.StringRelatedField(source='autorizada_por.get_full_name')
    tipo_dispositivo = serializers.StringRelatedField()
    url = serializers.StringRelatedField(source='get_absolute_url')
    url_salida = serializers.SerializerMethodField()
    no_salida_str = serializers.SerializerMethodField()

    class Meta:
        model = beqt_m.SolicitudMovimientoBeqt
        fields = '__all__'

    def get_no_salida_str(self, obj):
        if obj.no_salida != None:
            return str(obj.no_salida)
        else: return None

    def get_url_salida(self, obj):
        if obj.no_salida != None:
            if obj.no_salida.en_creacion:
                return reverse_lazy('salidainventario_edit', kwargs={'pk': obj.no_salida.id})
            else:
                return reverse_lazy('salidainventario_detail', kwargs={'pk': obj.no_salida.id})        
        else: return None

