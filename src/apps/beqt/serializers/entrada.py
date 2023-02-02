from calendar import c
from rest_framework import serializers
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

#from apps.inventario import models as inv_m
from apps.beqt import models as beqt_m
from apps.kardex import models as kax_m
from django.contrib.auth.models import User


class EntradaDetalleSerializer(serializers.ModelSerializer):
    """ Serializer para generar informes de la :class:'EntradaDetalle'
    """

    tdispositivo = serializers.SerializerMethodField()
    tipo_entrada = serializers.StringRelatedField(source='entrada.tipo')
    usa_triage = serializers.StringRelatedField(source='tipo_dispositivo.usa_triage')
    # Campos contabilidad
    precio_unitario = serializers.DecimalField(max_digits=8, decimal_places=2, default=None)   
    precio_total = serializers.DecimalField(max_digits=10, decimal_places=2, default=None)
    # Registro
    creado_por = serializers.StringRelatedField(source='creado_por.get_full_name')
    update_url = serializers.SerializerMethodField(read_only=True)
    dispositivo_list = serializers.SerializerMethodField(read_only=True)    
    dispositivo_qr = serializers.SerializerMethodField(read_only=True)
    grupos = serializers.SerializerMethodField(read_only=True)    

    class Meta:
        model = beqt_m.EntradaDetalleBeqt
        fields = (
            'id',
            'entrada',
            'tipo_dispositivo',                       
            'total',
            'precio_unitario',          
            'precio_total',
            'creado_por',
            'tdispositivo',
            'update_url',
            'tipo_entrada',
            'dispositivos_creados',           
            'descripcion',
            'usa_triage',
            'dispositivo_qr',
            'qr_dispositivo',
            'dispositivo_list',
            'pendiente_autorizar',
            'autorizado',
            'grupos'
           
            )

    def get_tdispositivo(self, object):
        return object.tipo_dispositivo.tipo

    def get_update_url(self, object):
        return reverse_lazy('entradadetalle_beqt_update', kwargs={'pk': object.id})

    def get_dispositivo_qr(self, object):
        return reverse_lazy('imprimir_qr_beqt', kwargs={'pk': object.entrada, 'detalle': object.id})   

    def get_dispositivo_list(self, object):
        return reverse_lazy('detalles_dispositivos_beqt', kwargs={'pk': object.entrada, 'detalle': object.id}) 

    
    def get_grupos(self, object):
        """ Este  metodo sirver para obtener el usuario que se va a enviar al javascript para mostrar
            los botones de autorizado y revisado en el detalle de entrada
            si es admin enviara el numero 1 o 3  de regreso
            si es el sub jefe enviara el numero 2
            si es otro usuario envirara el numero 4 
        """
        contador = 4
        usuario = self.context.get('request',None).user
        grupos  = User.objects.get(username=usuario)        
        for data in grupos.groups.all().values():            
            if data['name'] == "inv_admin":                
                contador = data['id']
            elif data['name'] == "inv_sub_jefe":                
                contador = data['id']
        return contador        
               

class EntradaSerializer(serializers.ModelSerializer):
    """ Serializer para generar el infome de la `class`:`Entrada`
    """
    creada_por = serializers.StringRelatedField(source='creada_por.get_full_name')
    recibida_por = serializers.StringRelatedField(source='recibida_por.get_full_name')
    proveedor = serializers.StringRelatedField()
    en_creacion = serializers.SerializerMethodField()
    boton = serializers.StringRelatedField(source='creada_por.get_full_name')
    tipo = serializers.StringRelatedField()
    urlSi = serializers.StringRelatedField(source='get_absolute_url')
    urlNo = serializers.SerializerMethodField()

    class Meta:
        model = beqt_m.Entrada
        fields = (
            'id',
            'tipo',
            'fecha',
            'en_creacion',
            'creada_por',
            'recibida_por',
            'proveedor',
            'boton',
            'urlSi',
            'urlNo',
        )

    def get_en_creacion(sel, object):
        if object.en_creacion:
            return "Si"
        else:
            return "No"

    def get_urlNo(self, object):
        return reverse_lazy('entrada_beqt_detail', kwargs={'pk': object.id})
