from rest_framework import serializers

from apps.escuela.models import Escuela
from apps.users.models import Organizacion
from apps.main.serializers import DynamicFieldsModelSerializer

from apps.ie import models as ie_models


class OrganizacionSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    cantidad_laboratorios = serializers.SerializerMethodField()
    cantidad_computadoras = serializers.SerializerMethodField()

    class Meta:
        model = Organizacion
        fields = '__all__'

    def get_cantidad_laboratorios(self, obj):
        return obj.laboratorios.count()

    def get_cantidad_computadoras(self, obj):
        return sum(lab.cantidad_computadoras for lab in obj.laboratorios.all())


class LaboratorioSerializer(serializers.ModelSerializer):
    computadoras = serializers.IntegerField(source='cantidad_computadoras')
    departamento = serializers.StringRelatedField(source='escuela__municipio__departamento__nombre')
    area = serializers.StringRelatedField(source='escuela__area__area')
    organizacion = serializers.StringRelatedField(source='organizacion__nombre')
    ninas = serializers.IntegerField(source='poblacion__alumna')
    ninos = serializers.IntegerField(source='poblacion__alumno')

    class Meta:
        model = ie_models.Laboratorio
        fields = (
            'computadoras', 'area',
            'organizacion', 'fecha', 'departamento',
            'ninas', 'ninos')


class EscuelaSerializer(serializers.ModelSerializer):
    municipio = serializers.StringRelatedField(source='municipio.nombre')
    departamento = serializers.StringRelatedField(source='municipio.departamento')
    area = serializers.StringRelatedField()
    jornada = serializers.StringRelatedField()
    lat = serializers.DecimalField(source='mapa.lat', max_digits=15, decimal_places=12)
    lng = serializers.DecimalField(source='mapa.lng', max_digits=15, decimal_places=12)
    laboratorios = serializers.SerializerMethodField()

    class Meta:
        model = Escuela
        fields = ('municipio', 'departamento', 'area', 'jornada', 'lat', 'lng', 'laboratorios')

    def get_laboratorios(self, obj):
        return obj.laboratorios.count()


class GeografiaSerializer(serializers.ModelSerializer):
    departamento = serializers.StringRelatedField(source='municipio__departamento__nombre')
    sector = serializers.StringRelatedField(source='sector__sector')
    area = serializers.StringRelatedField(source='area__area')
    nivel = serializers.StringRelatedField(source='nivel__nivel')
    cantidad = serializers.IntegerField()

    class Meta:
        model = Escuela
        fields = ('departamento', 'nivel', 'area', 'sector', 'cantidad')
