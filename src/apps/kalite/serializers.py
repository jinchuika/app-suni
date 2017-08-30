from rest_framework import serializers
from apps.main.serializers import DynamicFieldsModelSerializer

from apps.kalite.models import Punteo, Evaluacion, Visita, Grado, EjerciciosGrado


class PunteoSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    multiplicador = serializers.IntegerField(read_only=True)

    class Meta:
        model = Punteo
        fields = '__all__'
        read_only_fields = ('id', 'evaluacion', 'indicador', 'multiplicador')


class EvaluacionSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    promedio = serializers.FloatField(read_only=True)

    class Meta:
        model = Evaluacion
        fields = '__all__'
        read_only_fields = ('id', 'visita', 'rubrica')


class VisitaSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    promedio = serializers.FloatField(read_only=True)

    class Meta:
        model = Visita
        fields = '__all__'
        read_only_fields = ('id', 'escuela')


class VisitaCalendarSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    capacitador = serializers.CharField(source='capacitador.get_full_name')
    start = serializers.DateField(source='fecha')

    class Meta:
        model = Visita
        fields = ('id', 'capacitador', 'start')


class EjerciciosGradoSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    url = serializers.CharField(source='get_api_url', read_only=True)
    grado_url = serializers.CharField(source='grado.get_api_url', read_only=True)

    class Meta:
        model = EjerciciosGrado
        fields = '__all__'


class GradoSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    url = serializers.CharField(source='get_api_url', read_only=True)
    ejercicios = EjerciciosGradoSerializer(many=True, read_only=True)
    alcanzados = serializers.IntegerField(read_only=True)
    nivelar = serializers.IntegerField(read_only=True)
    total_estudiantes = serializers.IntegerField(read_only=True)
    total_ejercicios = serializers.IntegerField(read_only=True)
    promedio_ejercicios = serializers.FloatField(read_only=True)
    promedio_alcanzados = serializers.FloatField(read_only=True)

    class Meta:
        model = Grado
        fields = '__all__'
