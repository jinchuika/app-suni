from rest_framework import serializers
from django.urls import reverse_lazy
from apps.inventario import models as inv_m
from django.contrib.auth.models import User


class SalidaInventarioSerializer(serializers.ModelSerializer):
    """Serializer para la :class: `SalidaInventario`"""
    tipo_salida = serializers.StringRelatedField()
    beneficiario = serializers.StringRelatedField()
    estado = serializers.StringRelatedField()
    url = serializers.StringRelatedField(source='get_absolute_url')
    escuela = serializers.StringRelatedField(source='escuela.codigo')
    detail_url = serializers.SerializerMethodField()
    escuela_url = serializers.StringRelatedField(source='escuela.get_absolute_url')
    precio_total = serializers.SerializerMethodField()
    grupos = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.SalidaInventario
        fields = '__all__'

    def get_detail_url(self, object):
        return reverse_lazy('salidainventario_detail', kwargs={'pk': object.id})
    
    def get_precio_total(self, object):        
        valor_salida = 0
        if (self.get_grupos(self) != 4):
            for  data in object.paquetes.all():            
                valor_salida = valor_salida + data.valor_paquete()
            return valor_salida

    def get_grupos(self, object):
        """ Este  metodo sirver para obtener el usuario que se va a enviar al javascript para mostrar
            los botones de autorizado y revisado en el detalle de entrada
            si es admin enviara el numero 20 de regreso
            si es contabilidad enviara el numero 24
            si es otro usuario envirara el numero 4 
        """
        contador = 4
        usuario = self.context.get('request',None).user
        grupos  = User.objects.get(username=usuario)        
        for data in grupos.groups.all().values():
            if data['name'] == "inv_admin":                
                contador = data['id']
            elif data['name'] == "inv_conta":                
                contador = data['id']
        return contador


class RevisionSalidaSerializer(serializers.ModelSerializer):
    """ Serializer para la :class:`RevisionSalida`
    """
    revisado_por = serializers.StringRelatedField(source='revisado_por.get_full_name')
    urlSalida = serializers.StringRelatedField(source='get_absolute_url')
    estado = serializers.StringRelatedField(source='salida.estado')
    no_salida = serializers.StringRelatedField(source='salida.no_salida')
    escuela_url = serializers.StringRelatedField(source='salida.escuela.get_absolute_url')
    escuela = serializers.StringRelatedField(source='salida.escuela.codigo')
    tipo_salida = serializers.StringRelatedField(source='salida.tipo_salida')
    beneficiario = serializers.StringRelatedField(source='salida.beneficiario')

    class Meta:
        model = inv_m.RevisionSalida
        fields = '__all__'
