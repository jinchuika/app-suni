from rest_framework import serializers
from django.urls import reverse_lazy
from apps.inventario import models as inv_m
from apps.beqt import models as beqt_m

class DispositivoSerializer(serializers.ModelSerializer):
    """Serializer para generar los datos que se consumiran en la app de la :class:`Dispositivo`
    """
    tipo = serializers.StringRelatedField(allow_null=True)
    estado = serializers.StringRelatedField()
    etapa = serializers.StringRelatedField()
    marca = serializers.StringRelatedField()
    modelo = serializers.StringRelatedField()    
    serie = serializers.StringRelatedField()
    clase = serializers.StringRelatedField()
    url = serializers.StringRelatedField(source='get_absolute_url')
    procesador = serializers.SerializerMethodField()

    class Meta:
        model = beqt_m.DispositivoBeqt
        fields = [
            'id',
            'triage',
            'tipo',
            'entrada',
            'estado',
            'etapa',
            'marca',
            'modelo',
            'serie',
            'clase',
            'tarima',
            'url',
            'procesador']    

    def get_procesador(self, obj):          
        if obj.tipo.id == 6:            
            cpu_procesador = inv_m.CPU.objects.get(triage= obj)  
            return str(cpu_procesador.procesador)
        elif obj.tipo.id == 4:
            tablet_procesador = inv_m.Tablet.objects.get(triage= obj)  
            return str(tablet_procesador.procesador)
        elif  obj.tipo.id == 7:
            laptop_procesador = inv_m.Laptop.objects.get(triage= obj)            
            return str(laptop_procesador.procesador) 
        else:
            return ""


class TarimaSerializer(serializers.ModelSerializer):
    """ Serializer para generar los datos del app  de la :class:`Tarima`
    """
    dispositivos = DispositivoSerializer(many=True)
    cantidad_dispositivos = serializers.IntegerField(source='dispositivos.count')    

    class Meta:
        model = inv_m.Tarima
        # fields = ['sector', 'codigo_qr', 'dispositivos', 'cantidad_dispositivos']
        fields = ['sector', 'codigo_qr', 'dispositivos', 'cantidad_dispositivos' ]


class SectorSerializer(serializers.ModelSerializer):
    """ Serializer para  generar los datos para app de la :class:`Sector`
    """
    id = serializers.StringRelatedField(source='__str__')
    dispositivos = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.Sector
        fields = ['id', 'sector', 'nivel', 'dispositivos']

    def get_dispositivos(self, obj, pk=None):
        lista_dispositivos = inv_m.Dispositivo.objects.filter(tarima__sector=obj)
        dispositivos_s = DispositivoSerializer(lista_dispositivos, many=True)
        return dispositivos_s.data
