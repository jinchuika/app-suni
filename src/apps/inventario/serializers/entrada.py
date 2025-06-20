from calendar import c
from rest_framework import serializers
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from apps.inventario import models as inv_m
from apps.kardex import models as kax_m
from django.contrib.auth.models import User


class EntradaDetalleSerializer(serializers.ModelSerializer):
    """ Serializer para generar informes de la :class:'EntradaDetalle'
    """

    tdispositivo = serializers.SerializerMethodField()
    tipo_entrada = serializers.StringRelatedField(source='entrada.tipo')
    usa_triage = serializers.StringRelatedField(source='tipo_dispositivo.usa_triage')
    # Campos contabilidad
    precio_unitario = serializers.DecimalField(max_digits=20, decimal_places=10,allow_null=True)
    #precio_descontado = serializers.DecimalField(max_digits=8, decimal_places=2,allow_null=True)
    #precio_total = serializers.DecimalField(max_digits=10, decimal_places=2,allow_null=True)   
    # Registro
    creado_por = serializers.StringRelatedField(source='creado_por.get_full_name')
    update_url = serializers.SerializerMethodField(read_only=True)
    dispositivo_list = serializers.SerializerMethodField(read_only=True)
    repuesto_list = serializers.SerializerMethodField(read_only=True)
    dispositivo_qr = serializers.SerializerMethodField(read_only=True)
    repuesto_qr = serializers.SerializerMethodField(read_only=True)
    # Kardex
    es_kardex = serializers.StringRelatedField(source='tipo_dispositivo.kardex')
    url_kardex = serializers.SerializerMethodField(read_only=True)
    # Desecho
    existencia_desecho = serializers.IntegerField(read_only=True)
    fecha_desecho = serializers.SerializerMethodField(read_only=True)
    grupos = serializers.SerializerMethodField(read_only=True)
    info_proyecto = serializers.StringRelatedField(source='proyecto',many=True)


    class Meta:
        model = inv_m.EntradaDetalle
        fields = (
            'id',
            'entrada',
            'tipo_dispositivo',
            'util',
            'repuesto',
            'desecho',
            'total',
            'precio_unitario',
            'precio_subtotal',
            'precio_descontado',
            'precio_total',
            'creado_por',
            'tdispositivo',
            'update_url',
            'tipo_entrada',
            'dispositivos_creados',
            'repuestos_creados',
            'descripcion',
            'usa_triage',
            'dispositivo_qr',
            'repuesto_qr',
            'qr_repuestos',
            'qr_dispositivo',
            'dispositivo_list',
            'repuesto_list',
            'enviar_kardex',
            'proveedor_kardex',
            'estado_kardex',
            'tipo_entrada_kardex',
            'ingresado_kardex',
            'url_kardex',
            'existencia_desecho',
            'es_kardex',
            'fecha_desecho',
            'autorizado',
            'pendiente_autorizar',
            'rechazada',
            'cant_rechazada',
            'grupos',
            'info_proyecto',
            'proyecto'
            )

    def get_tdispositivo(self, object):
        return object.tipo_dispositivo.tipo

    def get_update_url(self, object):
        return reverse_lazy('entradadetalle_update', kwargs={'pk': object.id})

    def get_dispositivo_qr(self, object):
        return reverse_lazy('imprimir_qr', kwargs={'pk': object.entrada, 'detalle': object.id})

    def get_repuesto_qr(self, object):
        return reverse_lazy('imprimir_repuesto', kwargs={'pk': object.entrada, 'detalle': object.id})

    def get_dispositivo_list(self, object):
        return reverse_lazy('detalles_dispositivos', kwargs={'pk': object.entrada, 'detalle': object.id})

    def get_repuesto_list(self, object):
        return reverse_lazy('detalles_repuesto', kwargs={'pk': object.entrada, 'detalle': object.id})

    def get_url_kardex(self, object):
        try:
            detalle_kardex = kax_m.Entrada.objects.get(inventario_entrada=object.entrada)
            if(object.tipo_dispositivo.usa_triage is False):
                return reverse_lazy('kardex_entrada_detail', kwargs={'pk': detalle_kardex.id})
            else:
                return ""
        except ObjectDoesNotExist as e:
            print("Aun no se a creado el detalle")

    def get_existencia_desecho(self, obj):
        inventario_desecho = obj.existencia_desecho.all()
        return inventario_desecho

    def get_fecha_desecho(self, obj):
         fecha = inv_m.DesechoComentario.objects.filter(entrada_detalle=obj.id).last()
         if fecha is None:
            return ""
         else:
            return fecha.fecha_revision.date()

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
    info_proyecto = serializers.StringRelatedField(source='proyecto',many=True)
    precio_total =serializers.SerializerMethodField()
    grupo = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.Entrada
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
            'info_proyecto',
            'precio_total',
            'grupo'
        )

    def get_en_creacion(sel, object):        
        if object.en_creacion:
            return "Si"
        else:
            
            return "No"

    def get_urlNo(self, object):
        return reverse_lazy('entrada_detail', kwargs={'pk': object.id})
    
    def get_precio_total(self, object):
        #print("Precio:", object.total)        
        return object.total

    def get_grupo(self, object):
        """ Este  metodo sirver para obtener el usuario que se va a enviar al javascript para mostrar
            los botones de autorizado y revisado en el detalle de entrada
            si es admin enviara el numero 20 de regreso
            si es Bodega enviara el numero 21
            si es contabilidad enviara el numero 24
            si es otro usuario envirara el numero 4 
        """
        contador = 4
        usuario = self.context.get('request',None).user
        grupos  = User.objects.get(username=usuario)        
        for data in grupos.groups.all().values():
            if data['name'] == "inv_admin":                
                contador = data['id']
            elif data['name'] == "inv_bodega":                
                contador = data['id']
            elif data['name'] == "inv_conta":                
                contador = data['id']
        return contador
