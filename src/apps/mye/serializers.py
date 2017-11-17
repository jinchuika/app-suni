from rest_framework import serializers
from apps.main.serializers import CalendarSerializer
from apps.mye import models as mye_models


class CooperanteSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = mye_models.Cooperante
        fields = '__all__'


class ProyectoSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = mye_models.Proyecto
        fields = '__all__'


class ValidacionCalendarSerializer(CalendarSerializer):
    start = serializers.DateField(source='fecha_equipamiento')
    tip_title = serializers.StringRelatedField(source='escuela.municipio')
    tip_text = serializers.StringRelatedField(source='escuela.direccion')

    class Meta:
        model = mye_models.Validacion
        fields = ('start', 'title', 'url', 'tip_title', 'tip_text')
            
