from rest_framework import serializers
from django.urls import reverse_lazy
from apps.inventario import models as inv_m
from .bodega import DispositivoSerializer
from django.core import serializers as serializers_django
from django.contrib.auth.models import User


class DispositivoPaqueteSerializer(serializers.ModelSerializer):
    """ Serializer para generar los datos que se mostraran de la :class:`DispositivoPaquete`
    """
    dispositivo = DispositivoSerializer()

    class Meta:
        model = inv_m.DispositivoPaquete
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
        model = inv_m.DispositivoPaquete
        fields = '__all__'


class PaqueteSerializer(serializers.ModelSerializer):
    """ Serializer para generar los datos que se mostraran de la :class:`Paquete`
    """
    asignacion = DispositivoPaqueteSerializer(many=True)
    id = serializers.StringRelatedField(source='__str__')
    id_paquete = serializers.StringRelatedField(source='id')
    tipo_paquete = serializers.StringRelatedField()
    usa_triage = serializers.StringRelatedField(source='tipo_paquete.tipo_dispositivo.usa_triage')
    urlPaquet = serializers.StringRelatedField(source='get_absolute_url')
    cantidad_dispositivos = serializers.SerializerMethodField()
    tipo_salida = serializers.StringRelatedField(source='salida.tipo_salida')
    url_detail = serializers.SerializerMethodField()
    revisado_conta = serializers.SerializerMethodField()
    control_calidad = serializers.SerializerMethodField()
    salida_caja = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.Paquete
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
            'revisado_conta',
            'asignacion',
            'control_calidad',
            'salida_caja'

            )

    def get_cantidad_dispositivos(self, obj, pk=None):
        numero_dispositivos = inv_m.DispositivoPaquete.objects.filter(paquete=obj).count()
        return numero_dispositivos
    
    def get_revisado_conta(self, obj, pk=None):
        dispositivo = inv_m.DispositivoPaquete.objects.filter(paquete=obj)
        for data in dispositivo:
            if data.aprobado is True and (data.dispositivo.etapa.id==5 or data.dispositivo.etapa.id==6):
                return True
            else:
                return False

    def get_url_detail(self, obj):
        return reverse_lazy('dispositivo_asignados', kwargs={'pk': obj.id})
    
    def get_control_calidad(self, obj, pk=None):
        usuario = self.context.get('request',None).user        
        grupos  = User.objects.get(username=usuario)        
        if grupos.groups.filter(id=26):
            return True
        else:
            return False
    
    def get_salida_caja(self, obj, pk=None):
        if(obj.salida.tipo_salida.id == 6  or obj.salida.tipo_salida=="Caja de repuesto") and obj.salida.en_creacion == False:
            return True
        else:
            return False
        
        
            
           
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
        model = inv_m.SolicitudMovimiento
        fields = '__all__'

    def get_no_salida_str(self, obj):
        if obj.no_salida != None:
            return str(obj.no_salida)
        elif obj.no_inventariointerno != None:
            return str(obj.no_inventariointerno)
        else: return None

    def get_url_salida(self, obj):
        if obj.no_salida != None:
            if obj.no_salida.en_creacion:
                return reverse_lazy('salidainventario_edit', kwargs={'pk': obj.no_salida.id})
            else:
                return reverse_lazy('salidainventario_detail', kwargs={'pk': obj.no_salida.id})
        elif obj.no_inventariointerno != None:
            if obj.no_inventariointerno.borrador:
                return reverse_lazy('inventariointerno_edit', kwargs={'pk': obj.no_inventariointerno.id})
            else:
                return reverse_lazy('inventariointerno_detail', kwargs={'pk': obj.no_inventariointerno.id})
        else: return None

