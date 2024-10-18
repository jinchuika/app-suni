from rest_framework import serializers
from apps.Evaluacion import models as eva_models 
from apps.cyd import models as cyd_models

class SedeSerializer(serializers.ModelSerializer):
    escuela = serializers.StringRelatedField(source='escuela_beneficiada.codigo')
    urlescuela = serializers.StringRelatedField(source='escuela_beneficiada.get_absolute_url')
    municipio= serializers.StringRelatedField(source='municipio.nombre')
    departamento = serializers.StringRelatedField(source='municipio.departamento')
    capacitador = serializers.StringRelatedField(source='capacitador.get_full_name')
    grupos = serializers.StringRelatedField(source='grupos.count')
    urlsede=serializers.StringRelatedField(source='get_absolute_url')
    fecha_creacion = serializers.DateTimeField(format='%Y')

    class Meta:
        model = cyd_models.Sede
        fields = '__all__'