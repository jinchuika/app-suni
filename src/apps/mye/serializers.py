from rest_framework import serializers
from apps.main.serializers import CalendarSerializer
from apps.escuela.serializers import EscuelaSerializer
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


class SolicitudSerializer(serializers.ModelSerializer):
    departamento = serializers.StringRelatedField(source='escuela.municipio.departamento')
    municipio = serializers.StringRelatedField(source='escuela.municipio.nombre')
    escuela = EscuelaSerializer(fields='nombre,codigo,url')
    requisitos = serializers.StringRelatedField(source='porcentaje_requisitos')
    alumnos = serializers.IntegerField(source='poblacion.total_alumno')
    maestros = serializers.IntegerField(source='poblacion.total_maestro')
    equipada = serializers.BooleanField(source='escuela.equipada')

    class Meta:
        model = mye_models.Solicitud
        fields = (
            'departamento',
            'municipio',
            'escuela',
            'requisitos',
            'alumnos',
            'maestros',
            'equipada',
            'fecha')
