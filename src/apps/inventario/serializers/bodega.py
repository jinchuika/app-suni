from rest_framework import serializers
from django.urls import reverse_lazy
from apps.inventario import models as inv_m
from .repuesto import RepuestoInventarioSerializer

#Cambio para TPE
class DispositivoSerializer(serializers.ModelSerializer):
    """Serializer para generar los datos que se consumiran en la app de la :class:`Dispositivo`
    """
    tipo = serializers.StringRelatedField(allow_null=True)
    estado = serializers.StringRelatedField()
    etapa = serializers.StringRelatedField()
    marca = serializers.StringRelatedField()
    modelo = serializers.StringRelatedField()
    puerto = serializers.SerializerMethodField(read_only=True)       
    serie = serializers.StringRelatedField()
    clase = serializers.StringRelatedField()
    url = serializers.StringRelatedField(source='get_absolute_url')
    fecha_desecho = serializers.SerializerMethodField(read_only=True)
    procesador = serializers.SerializerMethodField()

    class Meta:
        model = inv_m.Dispositivo
        fields = [
            'id',
            'triage',
            'tipo',
            'entrada',
            'estado',
            'etapa',
            'marca',
            'modelo',
            'puerto',
            'serie',
            'clase',
            'tarima',
            'url',
            'fecha_desecho',
            'procesador']

    def get_fecha_desecho(self, obj):
         fecha = inv_m.DesechoComentario.objects.filter(dispositivo=obj.id).last()        
         if fecha is None:
            return ""
         else:        
            return fecha.fecha_revision.date()

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

    def get_puerto(self, obj):
        try:
            puerto = (obj.puerto)
            return str(puerto)
        except:
            return ""



class TarimaSerializer(serializers.ModelSerializer):
    """ Serializer para generar los datos del app  de la :class:`Tarima`
    """
    dispositivos = DispositivoSerializer(many=True)
    repuestos = RepuestoInventarioSerializer(many=True)
    cantidad_dispositivos = serializers.IntegerField(source='dispositivos.count')
    cantidad_repuestos = serializers.IntegerField(source='repuestos.count')

    class Meta:
        model = inv_m.Tarima
        # fields = ['sector', 'codigo_qr', 'dispositivos', 'cantidad_dispositivos']
        fields = ['sector', 'codigo_qr', 'dispositivos', 'repuestos', 'cantidad_dispositivos', 'cantidad_repuestos']


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
